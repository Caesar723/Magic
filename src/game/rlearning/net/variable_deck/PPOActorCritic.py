import torch
import torch.nn as nn
from torch.distributions import Categorical
import math

class Actor(nn.Module):
    def __init__(self, config):
        super().__init__()

        actor_dim = config["actor_dim"]
        candidate_dim = config["candidate_dim"]
        pointer_dim = config.get("pointer_dim", actor_dim)

        self.query_proj = nn.Linear(actor_dim, pointer_dim)
        self.candidate_proj = nn.Linear(candidate_dim, pointer_dim)

        self.query_norm = nn.LayerNorm(pointer_dim)
        self.candidate_norm = nn.LayerNorm(pointer_dim)

        self.scale = math.sqrt(pointer_dim)

    def forward(self, actor_feature, candidates, candidate_mask):
        candidate_mask = candidate_mask.to(
            device=candidates.device,
            dtype=torch.bool,
        )
        query = self.query_norm(
            self.query_proj(actor_feature)
        )

        keys = self.candidate_norm(
            self.candidate_proj(candidates)
        )


        """
        logits[b, k] = sum(
            query[b, d] * keys[b, k, d]
            for d in range(D)
        )
        """
        logits = torch.einsum(
            "bd,bkd->bk",
            query,
            keys,
        ) / self.scale

        return logits.masked_fill(~candidate_mask, float("-inf"))

class Critic(nn.Module):
    def __init__(self, config):
        super().__init__()

        critic_dim = config["critic_dim"]
        hidden_dim = config.get("critic_hidden_dim", critic_dim)

        self.value_head = nn.Sequential(
            nn.LayerNorm(critic_dim),
            nn.Linear(critic_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, critic_feature):
        return self.value_head(critic_feature).squeeze(-1)