"""Auxiliary relation and attribute heads for CardFusion."""

import torch.nn as nn


class BindingPairHead(nn.Module):
    """Predict the parser's set of effect-target binding pairs from one card vector."""
    def __init__(self, d_model=128, num_effects=24, num_targets=21, dropout=0.1):
        """Build a small relation classifier without changing CardFusion's main output."""
        super().__init__()
        self.num_effects, self.num_targets = num_effects, num_targets
        self.net = nn.Sequential(nn.RMSNorm(d_model), nn.Linear(d_model, d_model), nn.SiLU(), nn.Dropout(dropout), nn.Linear(d_model, num_effects * num_targets))

    def forward(self, h_card):
        """Return raw logits shaped [batch, effect, target]."""
        return self.net(h_card).view(-1, self.num_effects, self.num_targets)


class CardAttributeHeads(nn.Module):
    """Recover card attributes from the fused vector without feeding them downstream."""
    def __init__(self, d_model=128, num_card_types=5, special_type_dim=20, dropout=0.1):
        """Build one compact shared trunk and the six requested attribute predictions."""
        super().__init__()
        self.trunk = nn.Sequential(nn.RMSNorm(d_model), nn.Linear(d_model, d_model), nn.SiLU(), nn.Dropout(dropout))
        self.card_type = nn.Linear(d_model, num_card_types)
        self.special_type = nn.Linear(d_model, special_type_dim)
        self.mana_cost = nn.Linear(d_model, 6)
        self.attack = nn.Linear(d_model, 1)
        self.defend = nn.Linear(d_model, 1)
        self.has_state = nn.Linear(d_model, 1)

    def forward(self, h_card):
        """Return logits for categorical fields and raw values for ordered quantities."""
        hidden = self.trunk(h_card)
        return {"card_type": self.card_type(hidden), "special_type": self.special_type(hidden), "mana_cost": self.mana_cost(hidden), "attack": self.attack(hidden).squeeze(-1), "defend": self.defend(hidden).squeeze(-1), "has_state": self.has_state(hidden).squeeze(-1)}
