import torch
import torch.nn as nn

from game.rlearning.net.state_space.StateEncoder import (
    StateTransformerEncoder,
    TokenTransitionStateDecoder,
)
from game.rlearning.states.state_space.specific_entity import (
    BOARD_ZONE_NAMES,
    CARD_ZONE_NAMES,
    ENTITY_ZONE_NAMES,
    LOCATION_NAMES,
)


# ============================================================
# State helpers
# ============================================================

def squeeze_entity_time_dim(state):
    """Remove the single replay time dimension from an entity state."""
    if state["global_state"].ndim == 2:
        return state

    def select_first_frame(value):
        if isinstance(value, dict):
            return {
                name: select_first_frame(item)
                for name, item in value.items()
            }
        return value[:, 0]

    return select_first_frame(state)


# ============================================================
# Entity state encoder
# ============================================================

class EntityStateTransformerEncoder(StateTransformerEncoder):
    """Encode all card zones with one shared card representation."""

    def __init__(self, config):
        super().__init__(config)

        self.zone_to_id = {
            "global": 0,
            **{
                zone_name: zone_index + 1
                for zone_index, zone_name in enumerate(ENTITY_ZONE_NAMES)
            },
        }
        self.zone_emb = nn.Embedding(len(self.zone_to_id), self.d_model)

    def _encode_cls_token(self, batch_size, device):
        cls = self.cls_token.expand(batch_size, 1, self.d_model)
        kind_ids = self.make_full_ids(
            batch_size,
            1,
            self.kind_to_id["cls"],
            device,
        )
        zone_ids = self.make_full_ids(
            batch_size,
            1,
            self.zone_to_id["global"],
            device,
        )
        owner_ids = self.make_full_ids(
            batch_size,
            1,
            self.owner_to_id["none"],
            device,
        )

        cls = (
            cls
            + self.kind_emb(kind_ids)
            + self.zone_emb(zone_ids)
            + self.owner_emb(owner_ids)
        )
        padding_mask = torch.zeros(
            batch_size,
            1,
            dtype=torch.bool,
            device=device,
        )
        return cls, padding_mask

    def _zone_owner(self, zone_name, state):
        if zone_name == "stack_cards":
            return state["stack_extra"]["player_one_hot"]
        if zone_name.startswith("oppo_"):
            return "oppo"
        return "self"

    def forward(self, state):
        state = squeeze_entity_time_dim(state)

        global_state = state["global_state"]
        batch_size = global_state.shape[0]
        device = global_state.device

        tokens = []
        masks = []
        spans = {}
        cursor = 0

        # 1. Global summary token.
        x, mask = self._encode_cls_token(batch_size, device)
        tokens.append(x)
        masks.append(mask)
        spans["cls"] = (cursor, cursor + x.shape[1])
        cursor += x.shape[1]

        # 2. Global scalar tokens, including the unchanged mana state.
        x, mask = self.encode_global_tokens(global_state)
        tokens.append(x)
        masks.append(mask)
        spans["global_state"] = (cursor, cursor + x.shape[1])
        cursor += x.shape[1]

        # 3. Cards outside the battlefield.
        for zone_name in CARD_ZONE_NAMES:
            x, mask = self.encode_card_zone(
                state["card_zones"][zone_name],
                zone_name=zone_name,
                owner=self._zone_owner(zone_name, state),
                is_board=False,
            )
            tokens.append(x)
            masks.append(mask)
            spans[zone_name] = (cursor, cursor + x.shape[1])
            cursor += x.shape[1]

        # 4. Creature and land permanents use the same card fields.
        for zone_name in BOARD_ZONE_NAMES:
            x, mask = self.encode_card_zone(
                state["board_zones"][zone_name],
                zone_name=zone_name,
                owner=self._zone_owner(zone_name, state),
                is_board=True,
            )
            tokens.append(x)
            masks.append(mask)
            spans[zone_name] = (cursor, cursor + x.shape[1])
            cursor += x.shape[1]

        # 5. Contextualize every entity jointly.
        all_tokens = torch.cat(tokens, dim=1)
        padding_mask = torch.cat(masks, dim=1)
        hidden = self.transformer(
            all_tokens,
            src_key_padding_mask=padding_mask,
        )
        hidden = self.final_norm(hidden)
        state_embedding = hidden[:, 0]

        return state_embedding, hidden, padding_mask, spans


# ============================================================
# Source-card transition decoder
# ============================================================

class EntityTransitionStateDecoder(TokenTransitionStateDecoder):
    """Predict the destination and dynamic state of each source card."""

    def __init__(self, config):
        super().__init__(config)

        num_locations = int(config.get("num_locations", len(LOCATION_NAMES)))
        if num_locations != len(LOCATION_NAMES):
            raise ValueError(
                "num_locations must match the entity location schema: "
                f"expected {len(LOCATION_NAMES)}, got {num_locations}."
            )

        self.num_locations = num_locations
        self.location_head = nn.Linear(self.d_model, num_locations)
        self.card_tapped_head = nn.Linear(self.d_model, 1)

    def decode_entity_zone(self, hidden):
        return {
            "destination_zone": self.location_head(hidden),
            "card_special_types": self.card_special_type_head(hidden),
            "card_atks": self.card_atk_head(hidden),
            "card_hps": self.card_hp_head(hidden),
            "card_has_state": self.card_has_state_head(hidden).squeeze(-1),
            "card_tapped": self.card_tapped_head(hidden).squeeze(-1),
        }

    def decode_by_spans(self, h_next_tokens, spans):
        prediction = {}

        # 1. Global values keep the original decoder and loss semantics.
        start, end = spans["global_state"]
        prediction["global_state"] = self.global_head(
            h_next_tokens[:, start:end]
        )

        # 2. Each output slot remains tied to its source card entity.
        prediction["card_zones"] = {}
        for zone_name in CARD_ZONE_NAMES:
            start, end = spans[zone_name]
            prediction["card_zones"][zone_name] = self.decode_entity_zone(
                h_next_tokens[:, start:end]
            )

        prediction["board_zones"] = {}
        for zone_name in BOARD_ZONE_NAMES:
            start, end = spans[zone_name]
            prediction["board_zones"][zone_name] = self.decode_entity_zone(
                h_next_tokens[:, start:end]
            )

        return prediction
