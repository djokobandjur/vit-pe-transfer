"""
Vision Transformer with configurable positional encoding.

Supports four PE strategies:
  - learned     : nn.Parameter, added to token embeddings
  - sinusoidal  : fixed sin/cos buffer, added to token embeddings
  - rope        : rotary position embedding, applied to Q and K in attention
  - alibi       : attention bias with linear slopes, added to attention logits

Architecture: ViT-Base
  - embed_dim   : 768
  - depth       : 12 transformer blocks
  - num_heads   : 12
  - mlp_ratio   : 4.0

Compatible with checkpoints trained with the layout:
  {checkpoint_root}/{pe_type}_seed{seed}/best_model.pth
"""

import math
import torch
import torch.nn as nn


# ----------------------------------------------------------------------
# Positional encoding modules
# ----------------------------------------------------------------------

class LearnedPE(nn.Module):
    """Learned positional embedding: nn.Parameter added to tokens."""

    def __init__(self, num_positions, embed_dim):
        super().__init__()
        self.pos_embed = nn.Parameter(torch.zeros(1, num_positions, embed_dim))
        nn.init.trunc_normal_(self.pos_embed, std=0.02)

    def forward(self, x):
        return x + self.pos_embed[:, : x.shape[1], :]


class SinusoidalPE(nn.Module):
    """Sinusoidal PE: fixed sin/cos buffer added to tokens."""

    def __init__(self, num_positions, embed_dim):
        super().__init__()
        position = torch.arange(num_positions).unsqueeze(1).float()
        div_term = torch.exp(
            torch.arange(0, embed_dim, 2).float() * -(math.log(10000.0) / embed_dim)
        )
        pe = torch.zeros(num_positions, embed_dim)
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        # Buffer name matches original training-time naming
        self.register_buffer("pe", pe.unsqueeze(0))

    def forward(self, x):
        return x + self.pe[:, : x.shape[1], :]


class RoPE(nn.Module):
    """Rotary positional embedding applied to Q and K."""

    def __init__(self, num_positions, head_dim):
        super().__init__()
        inv_freq = 1.0 / (10000 ** (torch.arange(0, head_dim, 2).float() / head_dim))
        self.register_buffer("inv_freq", inv_freq)

        positions = torch.arange(num_positions).float()
        freqs = torch.einsum("i,j->ij", positions, inv_freq)
        # Buffer names match original training-time naming (cos_cached/sin_cached)
        self.register_buffer("cos_cached", freqs.cos())
        self.register_buffer("sin_cached", freqs.sin())

    def rotate_half(self, x):
        x1 = x[..., : x.shape[-1] // 2]
        x2 = x[..., x.shape[-1] // 2 :]
        return torch.cat((-x2, x1), dim=-1)

    def forward(self, q, k, seq_len):
        cos = self.cos_cached[:seq_len].repeat(1, 2).unsqueeze(0).unsqueeze(0)
        sin = self.sin_cached[:seq_len].repeat(1, 2).unsqueeze(0).unsqueeze(0)
        q_rot = (q * cos) + (self.rotate_half(q) * sin)
        k_rot = (k * cos) + (self.rotate_half(k) * sin)
        return q_rot, k_rot


class ALiBi(nn.Module):
    """ALiBi: attention bias with per-head linear slopes."""

    def __init__(self, num_heads, num_positions):
        super().__init__()
        slopes = self._get_slopes(num_heads)
        self.register_buffer("slopes", slopes.view(1, num_heads, 1, 1))

        rel_dist = torch.arange(num_positions).unsqueeze(0) - torch.arange(num_positions).unsqueeze(1)
        rel_dist = rel_dist.abs().float().unsqueeze(0).unsqueeze(0)
        self.register_buffer("rel_dist", rel_dist)

    @staticmethod
    def _get_slopes(num_heads):
        def get_powers(n):
            start = 2 ** (-(2 ** -(math.log2(n) - 3)))
            ratio = start
            return [start * (ratio ** i) for i in range(n)]

        if math.log2(num_heads).is_integer():
            return torch.tensor(get_powers(num_heads))
        # Non-power-of-2 fallback
        closest = 2 ** math.floor(math.log2(num_heads))
        slopes = get_powers(closest)
        extra = get_powers(2 * closest)[0::2][: num_heads - closest]
        return torch.tensor(slopes + extra)

    def get_bias(self, seq_len):
        return -self.slopes * self.rel_dist[:, :, :seq_len, :seq_len]


# ----------------------------------------------------------------------
# Attention + Block
# ----------------------------------------------------------------------

class MultiHeadAttention(nn.Module):
    def __init__(self, embed_dim, num_heads, pe_type="learned", num_positions=197):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.scale = self.head_dim ** -0.5
        self.pe_type = pe_type

        self.qkv = nn.Linear(embed_dim, 3 * embed_dim)
        self.proj = nn.Linear(embed_dim, embed_dim)

        if pe_type == "rope":
            self.rope = RoPE(num_positions, self.head_dim)
        elif pe_type == "alibi":
            self.alibi = ALiBi(num_heads, num_positions)

    def forward(self, x, return_attention=False):
        B, N, C = x.shape
        qkv = self.qkv(x).reshape(B, N, 3, self.num_heads, self.head_dim)
        qkv = qkv.permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]

        if self.pe_type == "rope":
            q, k = self.rope(q, k, N)

        attn = (q @ k.transpose(-2, -1)) * self.scale

        if self.pe_type == "alibi":
            attn = attn + self.alibi.get_bias(N)

        attn_weights = attn.softmax(dim=-1)
        out = (attn_weights @ v).transpose(1, 2).reshape(B, N, C)
        out = self.proj(out)

        if return_attention:
            return out, attn_weights
        return out


class TransformerBlock(nn.Module):
    def __init__(self, embed_dim, num_heads, mlp_ratio=4.0, dropout=0.1,
                 pe_type="learned", num_positions=197):
        super().__init__()
        self.norm1 = nn.LayerNorm(embed_dim)
        self.attn = MultiHeadAttention(embed_dim, num_heads, pe_type, num_positions)
        self.norm2 = nn.LayerNorm(embed_dim)
        mlp_dim = int(embed_dim * mlp_ratio)
        self.mlp = nn.Sequential(
            nn.Linear(embed_dim, mlp_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(mlp_dim, embed_dim),
            nn.Dropout(dropout),
        )

    def forward(self, x, return_attention=False):
        if return_attention:
            attn_out, attn_weights = self.attn(self.norm1(x), return_attention=True)
            x = x + attn_out
            x = x + self.mlp(self.norm2(x))
            return x, attn_weights
        x = x + self.attn(self.norm1(x))
        x = x + self.mlp(self.norm2(x))
        return x


# ----------------------------------------------------------------------
# Patch embedding + ViT
# ----------------------------------------------------------------------

class PatchEmbed(nn.Module):
    def __init__(self, img_size=224, patch_size=16, in_chans=3, embed_dim=768):
        super().__init__()
        self.img_size = img_size
        self.patch_size = patch_size
        self.num_patches = (img_size // patch_size) ** 2
        self.proj = nn.Conv2d(in_chans, embed_dim, kernel_size=patch_size, stride=patch_size)

    def forward(self, x):
        return self.proj(x).flatten(2).transpose(1, 2)


class VisionTransformer(nn.Module):
    """ViT-Base with configurable positional encoding."""

    def __init__(self, img_size=224, patch_size=16, in_chans=3, num_classes=100,
                 embed_dim=768, depth=12, num_heads=12, mlp_ratio=4.0, dropout=0.1,
                 pe_type="learned"):
        super().__init__()
        self.pe_type = pe_type
        self.embed_dim = embed_dim

        self.patch_embed = PatchEmbed(img_size, patch_size, in_chans, embed_dim)
        num_patches = self.patch_embed.num_patches
        num_positions = num_patches + 1  # +1 for CLS token

        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        nn.init.trunc_normal_(self.cls_token, std=0.02)

        # PE module: only embedding-space PE has a dedicated module
        if pe_type == "learned":
            self.pos_encoding = LearnedPE(num_positions, embed_dim)
        elif pe_type == "sinusoidal":
            self.pos_encoding = SinusoidalPE(num_positions, embed_dim)
        # RoPE and ALiBi are inside attention; no top-level pos_encoding module

        self.dropout = nn.Dropout(dropout)
        self.blocks = nn.ModuleList([
            TransformerBlock(embed_dim, num_heads, mlp_ratio, dropout,
                             pe_type=pe_type, num_positions=num_positions)
            for _ in range(depth)
        ])
        self.norm = nn.LayerNorm(embed_dim)
        self.head = nn.Linear(embed_dim, num_classes)

    def forward_features(self, x):
        """Return penultimate features (CLS token after final norm)."""
        B = x.shape[0]
        x = self.patch_embed(x)
        x = torch.cat([self.cls_token.expand(B, -1, -1), x], dim=1)
        if hasattr(self, "pos_encoding"):
            x = self.pos_encoding(x)
        x = self.dropout(x)
        for block in self.blocks:
            x = block(x)
        x = self.norm(x)
        return x[:, 0]  # CLS token

    def forward(self, x):
        features = self.forward_features(x)
        return self.head(features)
