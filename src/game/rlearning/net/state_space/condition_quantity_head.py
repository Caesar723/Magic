import torch
import torch.nn as nn


class ConditionQuantityEffectHead(nn.Module):
    def __init__(self, d_model=128, max_damage=20, max_heal=20, max_draw=20):
        super().__init__()
        self.context = nn.Sequential(
            nn.Linear(d_model * 2, d_model),
            nn.LayerNorm(d_model),
            nn.GELU(),
        )
        self.damage_head = nn.Linear(d_model, max_damage + 1)
        self.heal_head = nn.Linear(d_model, max_heal + 1)
        self.draw_head = nn.Linear(d_model, max_draw + 1)

    def forward(self, global_tokens, transition_plan):
        player_tokens = global_tokens[:, :2]
        plan_context = transition_plan.mean(dim=1).unsqueeze(1)
        plan_context = plan_context.expand(-1, 2, -1)
        features = self.context(
            torch.cat([player_tokens, plan_context], dim=-1)
        )
        return {
            "damage_logits": self.damage_head(features),
            "heal_logits": self.heal_head(features),
            "draw_logits": self.draw_head(features),
        }