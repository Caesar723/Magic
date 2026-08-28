import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class SwiGLU(nn.Module):
    def __init__(self, dim, expansion=4):
        super().__init__()
        hidden = dim * expansion
        self.fc = nn.Linear(dim, hidden * 2)
        self.proj = nn.Linear(hidden, dim)

    def forward(self, x):
        a, b = self.fc(x).chunk(2, dim=-1)
        return self.proj(F.silu(a) * b)


class ResBlock(nn.Module):
    def __init__(self, dim, expansion=4):
        super().__init__()
        self.norm = nn.RMSNorm(dim)
        self.ffn = SwiGLU(dim, expansion)
        self.scale = nn.Parameter(torch.ones(dim) * 1e-2)

    def forward(self, x):
        return x + self.scale * self.ffn(self.norm(x))


class MLPEncoder(nn.Module):
    def __init__(self, in_dim, d_model, depth=2):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(in_dim, d_model),
            *[ResBlock(d_model) for _ in range(depth)],
            nn.RMSNorm(d_model)
        )

    def forward(self, x):
        return self.net(x)


class GaussianHead(nn.Module):
    def __init__(self, d_model, latent_dim):
        super().__init__()
        self.mean = nn.Linear(d_model, latent_dim)
        self.std_head = nn.Linear(d_model, latent_dim)  # 原来叫 logvar

    def forward(self, x):
        mean = self.mean(x)
        std = F.softplus(self.std_head(x)) + 1e-4
        return mean, std


class CardFusion(nn.Module):
    def __init__(self, config):
        super().__init__()

        text_dim = config["text_dim"]
        attr_dim = config["attr_dim"]
        d_model = config["d_model"]

        self.text_scale = nn.Parameter(torch.tensor(math.sqrt(text_dim)))
        self.attr_norm = nn.RMSNorm(attr_dim)

        self.encoder = MLPEncoder(
            text_dim + attr_dim,
            d_model,
            depth=2
        )

    def forward(self, h_text, h_card_attr):
        h_text = h_text * self.text_scale
        h_attr = self.attr_norm(h_card_attr)

        h = torch.cat([h_text, h_attr], dim=-1)

        return self.encoder(h)


class PriorEncoder(nn.Module):
    def __init__(self, config):
        super().__init__()

        d = config["d_model"]
        z = config["latent_dim"]

        self.encoder = MLPEncoder(
            d * 3,
            d,
            depth=2
        )

        self.head = GaussianHead(d, z)

        self.card_norm = nn.RMSNorm(d)
        self.action_norm = nn.RMSNorm(d)
        self.state_norm = nn.RMSNorm(d)

    def forward(self, h_card, h_action, h_state):
        h = torch.cat([self.card_norm(h_card), self.action_norm(h_action), self.state_norm(h_state)], dim=-1)
        return self.head(self.encoder(h))


class PosteriorEncoder(nn.Module):
    def __init__(self, config):
        super().__init__()

        d = config["d_model"]
        z = config["latent_dim"]

        self.encoder = MLPEncoder(
            d * 4,
            d,
            depth=2
        )

        self.head = GaussianHead(d, z)

        self.card_norm = nn.RMSNorm(d)
        self.action_norm = nn.RMSNorm(d)
        self.state_norm = nn.RMSNorm(d)


    def forward(self, h_card, h_action, h_s, h_s_next):
        h = torch.cat(
            [
                self.card_norm(h_card),
                self.action_norm(h_action),
                self.state_norm(h_s),
                self.state_norm(h_s_next),
            ],
            dim=-1,
        )
        return self.head(self.encoder(h))