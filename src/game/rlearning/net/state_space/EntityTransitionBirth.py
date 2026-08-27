"""Entity-transition decoder with global slots for newly created entities."""

import torch
import torch.nn as nn

from game.rlearning.net.state_space.EntityTransition import (
    EntityTransitionStateDecoder,
)


class EntityTransitionBirthStateDecoder(EntityTransitionStateDecoder):
    """Decode source-card transitions plus an unordered set of birth slots.

    Source-card outputs retain the source-aligned semantics of
    :class:`EntityTransitionStateDecoder`.  Birth slots are learned queries
    without a source-card identity; each can either stay empty or describe a
    newly created entity in any destination zone.
    """

    def __init__(self, config):
        super().__init__(config)

        self.num_birth_slots = int(config.get("num_birth_slots", 10))
        if self.num_birth_slots <= 0:
            raise ValueError("num_birth_slots must be positive.")

        self.birth_queries = nn.Parameter(
            torch.empty(1, self.num_birth_slots, self.d_model)
        )
        nn.init.normal_(self.birth_queries, mean=0.0, std=0.02)
        self.birth_presence_head = nn.Linear(self.d_model, 1)

    def decode_birth_slots(self, hidden):
        """Decode complete entity metadata for source-free created objects."""
        card_costs = self.card_cost_head(hidden).unflatten(
            -1,
            (self.num_card_costs, self.num_stat_classes),
        )
        return {
            "presence": self.birth_presence_head(hidden).squeeze(-1),
            "destination_zone": self.location_head(hidden),
            "card_types": self.card_type_head(hidden),
            "card_costs": card_costs,
            "card_special_types": self.card_special_type_head(hidden),
            "card_atks": self.card_atk_head(hidden),
            "card_hps": self.card_hp_head(hidden),
            "card_has_state": self.card_has_state_head(hidden).squeeze(-1),
            "card_tapped": self.card_tapped_head(hidden).squeeze(-1),
        }

    def forward(
        self,
        state_tokens,
        state_padding_mask,
        spans,
        transition_vec,
    ):
        """Decode existing source cards and source-free birth queries jointly."""
        transition_memory = self.make_transition_memory(transition_vec)
        batch_size = state_tokens.shape[0]

        birth_queries = self.birth_queries.expand(batch_size, -1, -1)
        birth_padding_mask = torch.zeros(
            batch_size,
            self.num_birth_slots,
            dtype=torch.bool,
            device=state_tokens.device,
        )
        # Keeping both kinds of queries in one decoder target lets births attend
        # to the current-state entities while preserving the old source spans.
        decoder_tokens = torch.cat([state_tokens, birth_queries], dim=1)
        decoder_padding_mask = torch.cat(
            [state_padding_mask, birth_padding_mask],
            dim=1,
        )
        hidden = self.decoder(
            tgt=decoder_tokens,
            memory=transition_memory,
            tgt_key_padding_mask=decoder_padding_mask,
        )
        hidden = self.final_norm(hidden)

        source_token_count = state_tokens.shape[1]
        prediction = self.decode_by_spans(hidden[:, :source_token_count], spans)
        prediction["births"] = self.decode_birth_slots(
            hidden[:, source_token_count:]
        )
        return prediction
