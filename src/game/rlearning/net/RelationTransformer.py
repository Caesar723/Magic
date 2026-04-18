import torch
import torch.nn as nn


class RelationMultiHeadAttention(nn.Module):
    def __init__(self, dim, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = dim // num_heads

        self.qkv = nn.Linear(dim, dim * 3)
        self.out = nn.Linear(dim, dim)

    def forward(self, x, padding_mask=None, attn_bias=None):
        B, N, D = x.shape

        qkv = self.qkv(x)
        qkv = qkv.reshape(B, N, 3, self.num_heads, self.head_dim)
        q, k, v = qkv.unbind(dim=2)

        attn = torch.einsum("bnhd,bmhd->bhnm", q, k) / (self.head_dim ** 0.5)

        # 加 graph bias
        if attn_bias is not None:
            attn = attn + attn_bias.unsqueeze(1)

        # padding mask
        if padding_mask is not None:
            attn = attn.masked_fill(
                padding_mask.unsqueeze(1).unsqueeze(2),
                float('-inf')
            )

        attn = torch.softmax(attn, dim=-1)

        out = torch.einsum("bhnm,bmhd->bnhd", attn, v)
        out = out.reshape(B, N, D)

        return self.out(out)


class RelationTransformerLayer(nn.Module):
    def __init__(self, dim, num_heads):
        super().__init__()
        self.attn = RelationMultiHeadAttention(dim, num_heads)

        self.norm1 = nn.LayerNorm(dim)

        self.ff = nn.Sequential(
            nn.Linear(dim, dim * 4),
            nn.GELU(),
            nn.Linear(dim * 4, dim)
        )

        self.norm2 = nn.LayerNorm(dim)

    def forward(self, x, padding_mask=None, attn_bias=None):
        x = x + self.attn(x, padding_mask, attn_bias)
        x = self.norm1(x)

        x = x + self.ff(x)
        x = self.norm2(x)

        return x
