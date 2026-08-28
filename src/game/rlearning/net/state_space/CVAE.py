import torch
import torch.nn as nn
import torch.nn.functional as F





class CardFusion(nn.Module):
    def __init__(self, config):
        super().__init__()

        text_dim = config["text_dim"]
        attr_dim = config["attr_dim"]
        hidden_dim = config["hidden_dim"]
        d_model = config["d_model"]

        self.net = nn.Sequential(
            nn.Linear(text_dim + attr_dim, hidden_dim),
            nn.GELU(),
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, d_model),
        )

    def forward(self, h_text, h_card_attr):
        h = torch.cat([h_text, h_card_attr], dim=-1)
        return self.net(h)


class PriorEncoder(nn.Module):
    def __init__(self, config):
        super().__init__()

        d_model = config["d_model"]
        latent_dim = config["latent_dim"]

        self.net = nn.Sequential(
            nn.Linear(d_model * 3, d_model * 2),
            nn.GELU(),
            nn.Linear(d_model * 2, d_model),
            nn.GELU(),
        )

        self.mean_head = nn.Linear(d_model, latent_dim)
        self.std_head = nn.Linear(d_model, latent_dim)

    def forward(self, h_card, h_action, h_state):
        h = torch.cat([h_card, h_action, h_state], dim=-1)
        h = self.net(h)

        mean = self.mean_head(h)
        std = F.softplus(self.std_head(h)) + 1e-4

        return mean, std



class PosteriorEncoder(nn.Module):
    def __init__(self, config):
        super().__init__()

        d_model = config["d_model"]
        latent_dim = config["latent_dim"]

        self.net = nn.Sequential(
            nn.Linear(d_model * 4, d_model * 2),
            nn.GELU(),
            nn.LayerNorm(d_model * 2),

            nn.Linear(d_model * 2, d_model),
            nn.GELU(),
        )

        self.mean_head = nn.Linear(d_model, latent_dim)
        self.std_head = nn.Linear(d_model, latent_dim)

    def forward(self, h_card, h_action, h_s, h_s_next):
        h = torch.cat(
            [h_card, h_action, h_s, h_s_next],
            dim=-1,
        )

        h = self.net(h)

        mean = self.mean_head(h)
        std = F.softplus(self.std_head(h)) + 1e-4

        return mean, std
