import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class TextEncoder(nn.Module):
    def __init__(self,config):
        super().__init__()
        self.config=config
        #vocab_size = 49408

        width = config["transformer_width"]
        self.token_embed=nn.Embedding(config["vocab_size"],width)
        

        self.positional_embedding = nn.Parameter(torch.empty(config["context_length"], width))
        nn.init.normal_(self.positional_embedding, std=0.01)

        encoder_layer=nn.TransformerEncoderLayer(
            d_model=width,
            nhead=config["n_heads"],
            dim_feedforward=width*4,
            dropout=config["dropout"],
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )


        
        self.encoder_layers=nn.TransformerEncoder(
            encoder_layer,
            num_layers=config["n_layers"]
        )

        self.ln_final = nn.LayerNorm(config["transformer_width"])
        
    
        self.text_projection = nn.Parameter(
            torch.empty(width, config["embed_dim"])
        )
        nn.init.normal_(self.text_projection, std=width ** -0.5)



    def forward(self, input_ids, src_key_padding_mask=None):
        x = self.token_embed(input_ids)

        batch_size, seq_len = input_ids.shape

        x = x + self.positional_embedding[:seq_len, :].to(
            dtype=x.dtype,
            device=x.device
        )

        causal_mask = self.build_causal_mask(seq_len, x.device)

        x = self.encoder_layers(
            x,
            mask=causal_mask,
            src_key_padding_mask=src_key_padding_mask,
        )

        x = self.ln_final(x)
        eot_indices = input_ids.argmax(dim=-1)
        x = x[torch.arange(batch_size, device=x.device), eot_indices]

        x = x @ self.text_projection
        x = F.normalize(x, dim=-1)
        return x

    def build_causal_mask(self, seq_len, device):
        mask = torch.empty(seq_len, seq_len, device=device)
        mask.fill_(float("-inf"))
        mask.triu_(1)
        return mask

class CardStateEncoder(nn.Module):
    def __init__(self, config):
        super().__init__()

        self.type_embed = nn.Embedding(config["max_card_type"], config["output_dim"])
        self.special_type_proj = nn.Sequential(
            nn.Linear(config["num_special"], config["output_dim"]),
            nn.LayerNorm(config["output_dim"]),
            nn.GELU(),
            nn.Linear(config["output_dim"], config["output_dim"]),
        )
        self.mana_encoder = nn.Sequential(
            nn.Linear(6, config["output_dim"]),
            nn.LayerNorm(config["output_dim"]),
            nn.GELU(),
            nn.Linear(config["output_dim"], config["output_dim"]),
        )
        self.color_encoder = nn.Sequential(
            nn.Linear(5, config["output_dim"]),
            nn.LayerNorm(config["output_dim"]),
            nn.GELU(),
            nn.Linear(config["output_dim"], config["output_dim"]),
        )

        self.has_combat_embed = nn.Embedding(2, config["output_dim"])

        self.combat_mlp = nn.Sequential(
            nn.Linear(2, config["output_dim"]),
            nn.GELU(),
            nn.Linear(config["output_dim"], config["output_dim"])
        )

        self.out = nn.Sequential(
            nn.Linear(config["output_dim"] * 6, config["output_dim"]),
            nn.GELU(),
            nn.Linear(config["output_dim"], config["output_dim"])
        )


        


    def forward(self, card_type, special_type, mana_cost, attack, defense, has_combat, color_identity):
        """Encode structured card facts before CardFusion joins them with text."""
        type_feat = self.type_embed(card_type)
        special_feat = self.special_type_proj(special_type.float())
        mana_feat = self.mana_encoder(mana_cost.float())
        color_feat = self.color_encoder(color_identity.float())

        combat_raw = torch.stack([attack, defense], dim=-1)
        combat_feat = self.combat_mlp(combat_raw)

        combat_feat = combat_feat * has_combat.unsqueeze(-1).float()

        has_combat_feat = self.has_combat_embed(has_combat.long())

        x = torch.cat([
            type_feat,
            special_feat,
            mana_feat,
            color_feat,
            combat_feat,
            has_combat_feat,
        ], dim=-1)

        return self.out(x)

class CardBoardStateEncoder(nn.Module):
    def __init__(self, config):
        super().__init__()

        
        self.special_type_embed= nn.Embedding(config["num_special"], config["output_dim"])
        
        self.combat_mlp = nn.Sequential(
            nn.Linear(2, config["output_dim"]),
            nn.GELU(),
            nn.Linear(config["output_dim"], config["output_dim"])
        )

        self.out = nn.Sequential(
            nn.Linear(config["output_dim"] * 2, config["output_dim"]),
            nn.GELU(),
            nn.Linear(config["output_dim"], config["output_dim"])
        )


        


    def forward(self,special_type, attack, defense):
        
        special_feat = self.special_type_embed(special_type)
        
        combat_raw = torch.stack([attack, defense], dim=-1)
        combat_feat = self.combat_mlp(combat_raw)

        combat_feat = combat_feat

        
        x = torch.cat([
            special_feat,
            combat_feat,
        ], dim=-1)

        return self.out(x)


class ActionEncoder(nn.Module):
    def __init__(self, config):
        super().__init__()

        d = config["output_dim"]

        self.action_embed = nn.Embedding(
            config["action_size"],  # 33
            d
        )

        self.out = nn.Sequential(
            nn.LayerNorm(d),
            nn.Linear(d, d),
            nn.GELU(),
            nn.Linear(d, d),
        )

    def forward(self, action):
        action_feat = self.action_embed(action.long())
        return self.out(action_feat)

def squeeze_time_dim_state(state):
    """
    把 [B, 1, ...] 变成 [B, ...]。

    当前版本假设 T=1。
    如果之后你想用多帧历史，可以改成把 T 和 slot 合并。
    """
    if state["global_state"].ndim == 2:
        return state

    out = {}

    out["global_state"] = state["global_state"][:, 0]

    out["card_zones"] = {}
    for zone_name, zone in state["card_zones"].items():
        out["card_zones"][zone_name] = {
            k: v[:, 0]
            for k, v in zone.items()
        }

    out["board_zones"] = {}
    for zone_name, zone in state["board_zones"].items():
        out["board_zones"][zone_name] = {
            k: v[:, 0]
            for k, v in zone.items()
        }

    out["stack_extra"] = {
        k: v[:, 0]
        for k, v in state["stack_extra"].items()
    }

    return out


class StateTransformerEncoder(nn.Module):
    def __init__(
        self,
        config: dict,
    ):
        super().__init__()

        num_card_types = config["num_card_types"]
        special_type_dim = config["special_type_dim"]
        stack_player_dim = config["stack_player_dim"]
        stack_action_vocab_size = config["stack_action_vocab_size"]
        d_model = config["d_model"]
        nhead = config["nhead"]
        num_layers = config["num_layers"]
        dim_feedforward = config["dim_feedforward"]
        dropout = config["dropout"]
        max_slots = config["max_slots"]


        self.d_model = d_model
        self.special_type_dim = special_type_dim
        self.use_base_stats = bool(config.get("use_base_stats", False))

        # =====================================================
        # token category ids
        # =====================================================

        self.zone_to_id = {
            "global": 0,
            "hand": 1,
            "library": 2,
            "graveyard": 3,
            "stack_cards": 4,
            "self_board": 5,
            "oppo_board": 6,
        }

        self.kind_to_id = {
            "cls": 0,
            "scalar": 1,
            "card": 2,
            "board_card": 3,
            "stack_extra": 4,
        }

        self.owner_to_id = {
            "none": 0,
            "self": 1,
            "oppo": 2,
        }

        # =====================================================
        # learnable structure embeddings
        # =====================================================

        self.cls_token = nn.Parameter(
            torch.zeros(1, 1, d_model)
        )

        self.zone_emb = nn.Embedding(
            len(self.zone_to_id),
            d_model,
        )

        self.kind_emb = nn.Embedding(
            len(self.kind_to_id),
            d_model,
        )

        self.owner_emb = nn.Embedding(
            len(self.owner_to_id),
            d_model,
        )

        self.slot_pos_emb = nn.Embedding(
            max_slots,
            d_model,
        )

        # scalar name ids for global channels:
        # 0 = self_life, 1 = oppo_life, 2..7 = mana C/U/W/B/R/G
        self.scalar_name_emb = nn.Embedding(
            16,
            d_model,
        )

        # =====================================================
        # content encoders
        # =====================================================

        self.scalar_value_proj = nn.Sequential(
            nn.Linear(1, d_model),
            nn.GELU(),
            nn.LayerNorm(d_model),
        )

        self.card_type_emb = nn.Embedding(
            num_card_types + 1,
            d_model,
        )

        self.card_special_type_proj = nn.Sequential(
            nn.Linear(special_type_dim, d_model),
            nn.GELU(),
            nn.LayerNorm(d_model),
        )

        self.card_cost_proj = nn.Sequential(
            nn.Linear(6, d_model),
            nn.GELU(),
            nn.LayerNorm(d_model),
        )
        self.card_color_proj = nn.Sequential(
            nn.Linear(5, d_model),
            nn.GELU(),
            nn.LayerNorm(d_model),
        )

        # atk, hp, has_state
        self.card_numeric_proj = nn.Sequential(
            nn.Linear(3, d_model),
            nn.GELU(),
            nn.LayerNorm(d_model),
        )
        if self.use_base_stats:
            self.card_base_stat_proj = nn.Sequential(
                nn.Linear(2, d_model),
                nn.GELU(),
                nn.LayerNorm(d_model),
            )

        self.card_attacker_emb = nn.Embedding(2, d_model, padding_idx=0)

        self.stack_player_proj = nn.Sequential(
            nn.Linear(stack_player_dim, d_model),
            nn.GELU(),
            nn.LayerNorm(d_model),
        )

        self.stack_action_emb = nn.Embedding(
            stack_action_vocab_size + 1,
            d_model,
        )

        # =====================================================
        # transformer encoder
        # =====================================================

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers,
        )

        self.final_norm = nn.LayerNorm(d_model)

    # =========================================================
    # helper
    # =========================================================

    def make_full_ids(self, B, N, value, device):
        return torch.full(
            (B, N),
            value,
            dtype=torch.long,
            device=device,
        )
    def owner_ids_from_player_one_hot(self, player_one_hot, num_slots=None):
        """
        支持：
        [B, 2]    -> [B] 或扩展为 [B, N]
        [B, N, 2] -> [B, N]
        """
        player_one_hot = player_one_hot.float()

        if player_one_hot.ndim == 2:
            B, _ = player_one_hot.shape

            owner_ids = torch.full(
                (B,),
                self.owner_to_id["none"],
                dtype=torch.long,
                device=player_one_hot.device,
            )

            self_mask = player_one_hot[:, 0] > 0.5
            oppo_mask = player_one_hot[:, 1] > 0.5

            owner_ids[self_mask] = self.owner_to_id["self"]
            owner_ids[oppo_mask] = self.owner_to_id["oppo"]

            if num_slots is not None:
                owner_ids = owner_ids.unsqueeze(1).expand(B, num_slots)

            return owner_ids

        if player_one_hot.ndim == 3:
            B, N, _ = player_one_hot.shape

            owner_ids = torch.full(
                (B, N),
                self.owner_to_id["none"],
                dtype=torch.long,
                device=player_one_hot.device,
            )

            self_mask = player_one_hot[..., 0] > 0.5
            oppo_mask = player_one_hot[..., 1] > 0.5

            owner_ids[self_mask] = self.owner_to_id["self"]
            owner_ids[oppo_mask] = self.owner_to_id["oppo"]

            return owner_ids

        

    # =========================================================
    # global scalar tokens
    # =========================================================

    def encode_global_tokens(self, global_state):
        """
        global_state: [B, G]
            G = 8 = self_life + oppo_life + self_mana(C,U,W,B,R,G)

        token: one scalar token per channel

        return:
            x:    [B, G, D]
            mask: [B, G]
        """
        B, G = global_state.shape
        device = global_state.device

        values = global_state.float().unsqueeze(-1)  # [B, G, 1]

        scalar_ids = torch.arange(
            G,
            device=device,
            dtype=torch.long,
        ).unsqueeze(0).expand(B, G)

        value_emb = self.scalar_value_proj(values)
        name_emb = self.scalar_name_emb(scalar_ids)

        zone_ids = self.make_full_ids(
            B,
            G,
            self.zone_to_id["global"],
            device,
        )

        kind_ids = self.make_full_ids(
            B,
            G,
            self.kind_to_id["scalar"],
            device,
        )

        one_hot=torch.zeros(G, 2, device=device)
        one_hot[0, 0] = 1
        one_hot[1, 1] = 1
        one_hot[2, 0] = 1
        owner_ids = self.owner_ids_from_player_one_hot(
            one_hot,
            
        )

        # print(value_emb.shape, name_emb.shape, zone_ids.shape, kind_ids.shape, owner_ids.shape)
        # print(self.owner_emb(owner_ids).shape)

        x = (
            value_emb
            + name_emb
            + self.zone_emb(zone_ids)
            + self.kind_emb(kind_ids)
            + self.owner_emb(owner_ids)
        )

        # global tokens 永远有效
        mask = torch.zeros(
            B,
            G,
            dtype=torch.bool,
            device=device,
        )

        return x, mask

    # =========================================================
    # card zone tokens
    # =========================================================

    def encode_card_zone(
        self,
        zone,
        zone_name: str,
        owner: "str|torch.Tensor",
        is_board: bool,
    ):
        """
        普通区域:
            hand / library / graveyard / stack_cards

        board 区域:
            self_board / oppo_board

        zone:
            card_types:         [B, N]      可选
            card_costs:         [B, N, 6]   可选
            card_color_identity:[B, N, 5]   可选，U/W/B/R/G
            card_special_types: [B, N, K]
            card_atks:          [B, N]
            card_hps:           [B, N]
            card_base_atks:     [B, N]      optional
            card_base_hps:      [B, N]      optional
            card_has_state:     [B, N]
            card_is_attacker:   [B, N]
            card_mask:          [B, N]

        return:
            x:    [B, N, D]
            mask: [B, N]
        """
        device = zone["card_mask"].device
        B, N = zone["card_mask"].shape

        # PyTorch Transformer:
        #   True  = ignore / padding
        #   False = valid token
        padding_mask = zone["card_mask"].float() <= 0

        # -----------------------------------------------------
        # card type
        # -----------------------------------------------------
        if "card_types" in zone:
            card_types = zone["card_types"].long()
        else:
            # board 目前没有 card_types，所以用 0 表示 unknown
            card_types = torch.zeros(
                B,
                N,
                dtype=torch.long,
                device=device,
            )

        card_type_emb = self.card_type_emb(card_types)

        # -----------------------------------------------------
        # special type
        # -----------------------------------------------------
        special_type = zone["card_special_types"].float()
        special_type_emb = self.card_special_type_proj(special_type)

        # -----------------------------------------------------
        # numeric features
        # -----------------------------------------------------
        def get_scalar(name,unsqueeze=True,dim=1):
            if name in zone:
                x = zone[name].float()
                if unsqueeze:
                    return x.unsqueeze(-1)
                else:
                    return x
            else:
                x = torch.zeros(
                    B,
                    N,
                    dim,
                    dtype=torch.float32,
                    device=device,
                )
                return x
            

        card_costs = get_scalar("card_costs",unsqueeze=False,dim=6)
        card_colors = get_scalar("card_color_identity",unsqueeze=False,dim=5)
        card_atks = get_scalar("card_atks")
        card_hps = get_scalar("card_hps")
        card_has_state = get_scalar("card_has_state")
        card_is_attacker = get_scalar("card_is_attacker").squeeze(-1).long().clamp(0, 1)

        numeric = torch.cat(
            [
                card_atks,
                card_hps,
                card_has_state,
            ],
            dim=-1,
        )

        numeric_emb = self.card_numeric_proj(numeric)
        card_cost_emb = self.card_cost_proj(card_costs)
        card_color_emb = self.card_color_proj(card_colors)

        # -----------------------------------------------------
        # content embedding
        # -----------------------------------------------------
        x = card_type_emb + special_type_emb + numeric_emb + card_cost_emb + card_color_emb
        x = x + self.card_attacker_emb(card_is_attacker)
        if self.use_base_stats:
            base_stats = torch.cat(
                [get_scalar("card_base_atks"), get_scalar("card_base_hps")],
                dim=-1,
            )
            x = x + self.card_base_stat_proj(base_stats)

        # -----------------------------------------------------
        # structural embeddings
        # -----------------------------------------------------
        zone_ids = self.make_full_ids(
            B,
            N,
            self.zone_to_id[zone_name],
            device,
        )

        kind_name = "board_card" if is_board else "card"

        kind_ids = self.make_full_ids(
            B,
            N,
            self.kind_to_id[kind_name],
            device,
        )

        if isinstance(owner, str):
            owner_ids = self.make_full_ids(
                B,
                N,
                self.owner_to_id[owner],
                device,
            )
        else:
            owner_ids = self.owner_ids_from_player_one_hot(owner)

        slot_ids = torch.arange(
            N,
            device=device,
            dtype=torch.long,
        ).unsqueeze(0).expand(B, N)

        x = (
            x
            + self.zone_emb(zone_ids)
            + self.kind_emb(kind_ids)
            + self.owner_emb(owner_ids)
            + self.slot_pos_emb(slot_ids)
        )

        return x, padding_mask



    # =========================================================
    # forward
    # =========================================================

    def forward(self, state):
        """
        state:
            nested tensor dict

        return:
            state_emb:    [B, D]
            all_tokens:   [B, L, D]
            padding_mask: [B, L]
        """
        state = squeeze_time_dim_state(state)

        global_state = state["global_state"]
        B = global_state.shape[0]
        device = global_state.device

        tokens = []
        masks = []
        spans = {}
        cursor = 0

        # -----------------------------------------------------
        # CLS token
        # -----------------------------------------------------
        cls = self.cls_token.expand(B, 1, self.d_model)

        cls_kind_ids = self.make_full_ids(
            B,
            1,
            self.kind_to_id["cls"],
            device,
        )

        cls_zone_ids = self.make_full_ids(
            B,
            1,
            self.zone_to_id["global"],
            device,
        )

        cls_owner_ids = self.make_full_ids(
            B,
            1,
            self.owner_to_id["none"],
            device,
        )

        cls = (
            cls
            + self.kind_emb(cls_kind_ids)
            + self.zone_emb(cls_zone_ids)
            + self.owner_emb(cls_owner_ids)
        )

        cls_mask = torch.zeros(
            B,
            1,
            dtype=torch.bool,
            device=device,
        )

        tokens.append(cls)
        masks.append(cls_mask)
        spans["cls"] = (cursor, cursor + 1)
        cursor += 1

        # -----------------------------------------------------
        # global scalar tokens
        # -----------------------------------------------------
        x, m = self.encode_global_tokens(
            state["global_state"]
        )
        tokens.append(x)
        masks.append(m)
        spans["global_state"] = (cursor, cursor + x.shape[1])
        cursor += x.shape[1]

        # -----------------------------------------------------
        # hand / library / graveyard / stack cards
        # -----------------------------------------------------
        card_zones = state["card_zones"]

        x, m = self.encode_card_zone(
            card_zones["hand"],
            zone_name="hand",
            owner="self",
            is_board=False,
        )
        tokens.append(x)
        masks.append(m)
        spans["hand"] = (cursor, cursor + x.shape[1])
        cursor += x.shape[1]

        x, m = self.encode_card_zone(
            card_zones["library"],
            zone_name="library",
            owner="self",
            is_board=False,
        )
        tokens.append(x)
        masks.append(m)
        spans["library"] = (cursor, cursor + x.shape[1])
        cursor += x.shape[1]

        x, m = self.encode_card_zone(
            card_zones["graveyard"],
            zone_name="graveyard",
            owner="self",
            is_board=False,
        )
        tokens.append(x)
        masks.append(m)
        spans["graveyard"] = (cursor, cursor + x.shape[1])
        cursor += x.shape[1]

        x, m = self.encode_card_zone(
            card_zones["stack_cards"],
            zone_name="stack_cards",
            owner=state["stack_extra"]["player_one_hot"],
            is_board=False,
        )
        tokens.append(x)
        masks.append(m)
        spans["stack_cards"] = (cursor, cursor + x.shape[1])
        cursor += x.shape[1]

        # -----------------------------------------------------
        # board tokens
        # -----------------------------------------------------
        board_zones = state["board_zones"]

        x, m = self.encode_card_zone(
            board_zones["self_board"],
            zone_name="self_board",
            owner="self",
            is_board=True,
        )
        tokens.append(x)
        masks.append(m)
        spans["self_board"] = (cursor, cursor + x.shape[1])
        cursor += x.shape[1]

        x, m = self.encode_card_zone(
            board_zones["oppo_board"],
            zone_name="oppo_board",
            owner="oppo",
            is_board=True,
        )
        tokens.append(x)
        masks.append(m)

        spans["oppo_board"] = (cursor, cursor + x.shape[1])
        cursor += x.shape[1]

        # -----------------------------------------------------
        # concat all tokens
        # -----------------------------------------------------
        all_tokens = torch.cat(tokens, dim=1)       # [B, L, D]
        padding_mask = torch.cat(masks, dim=1)      # [B, L]

        # -----------------------------------------------------
        # transformer
        # -----------------------------------------------------
        h = self.transformer(
            all_tokens,
            src_key_padding_mask=padding_mask,
        )

        h = self.final_norm(h)

        # CLS 作为整个 state 的 embedding
        state_emb = h[:, 0]

        return state_emb, h, padding_mask, spans


class TokenTransitionStateDecoder(nn.Module):
    def __init__(self, config: dict):
        super().__init__()

        transition_dim = config["transition_dim"]
        num_card_types = config["num_card_types"]
        num_card_costs = config["num_card_costs"]
        special_type_dim = config["special_type_dim"]
        stack_player_dim = config["stack_player_dim"]
        stack_action_vocab_size = config["stack_action_vocab_size"]
        d_model = config["d_model"]
        transition_memory_len = config["transition_memory_len"]
        nhead = config["nhead"]
        num_layers = config["num_layers"]
        dim_feedforward = config["dim_feedforward"]
        dropout = config["dropout"]
        num_stat_classes = config["num_stat_classes"]

        self.num_card_types = num_card_types
        self.num_card_costs = num_card_costs
        self.num_stat_classes = num_stat_classes
        self.special_type_dim = special_type_dim
        self.stack_player_dim = stack_player_dim
        self.stack_action_vocab_size = stack_action_vocab_size
        self.d_model = d_model

        self.transition_memory_len = transition_memory_len

        self.z_to_transition_memory = nn.Sequential(
            nn.Linear(transition_dim, d_model * 2),
            nn.GELU(),
            nn.Linear(
                d_model * 2,
                self.transition_memory_len * d_model,
            ),
        )

        self.transition_memory_pos = nn.Parameter(
            torch.zeros(
                1,
                self.transition_memory_len,
                d_model,
            )
        )

        self.transition_memory_norm = nn.LayerNorm(d_model)

        decoder_layer = nn.TransformerDecoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )

        self.decoder = nn.TransformerDecoder(
            decoder_layer,
            num_layers=num_layers,
        )

        self.final_norm = nn.LayerNorm(d_model)

        # =====================================================
        # heads
        # =====================================================

        # Global values and card stats share the same discrete value classes.
        self.global_head = nn.Linear(d_model, num_stat_classes)

        # card zones
        self.card_type_head = nn.Linear(d_model, num_card_types)
        self.card_cost_head = nn.Linear(
            d_model,
            num_card_costs * num_stat_classes,
        )
        self.card_special_type_head = nn.Linear(d_model, special_type_dim)
        self.card_atk_head = nn.Linear(d_model, num_stat_classes)
        self.card_hp_head = nn.Linear(d_model, num_stat_classes)
        self.card_has_state_head = nn.Linear(d_model, 1)
        self.card_mask_head = nn.Linear(d_model, 1)

        # stack extra
        self.stack_player_head = nn.Linear(d_model, stack_player_dim)
        self.stack_action_head = nn.Linear(d_model, stack_action_vocab_size)

    def make_transition_memory(self, z):
        """
        z:
            [B, latent_dim]

        return:
            transition_memory:
                [B, M, D]
        """
        B = z.shape[0]

        x = self.z_to_transition_memory(z)

        x = x.view(
            B,
            self.transition_memory_len,
            self.d_model,
        )

        x = x + self.transition_memory_pos
        x = self.transition_memory_norm(x)

        return x

    def decode_card_zone(self, h_zone):
        """
        h_zone: [B, N, D]
        """
        card_costs = self.card_cost_head(h_zone).unflatten(
            -1,
            (self.num_card_costs, self.num_stat_classes),
        )
        return {
            "card_types": self.card_type_head(h_zone),
            "card_costs": card_costs,
            "card_atks": self.card_atk_head(h_zone),
            "card_hps": self.card_hp_head(h_zone),
            "card_special_types": self.card_special_type_head(h_zone),
            "card_has_state": self.card_has_state_head(h_zone).squeeze(-1),
            "card_mask": self.card_mask_head(h_zone).squeeze(-1),
        }

    def decode_board_zone(self, h_zone):
        """
        你目前 board 没有 card_types / card_costs。
        如果之后加了，建议直接复用 decode_card_zone。
        """
        return {
            "card_special_types": self.card_special_type_head(h_zone),
            "card_atks": self.card_atk_head(h_zone),
            "card_hps": self.card_hp_head(h_zone),
            "card_has_state": self.card_has_state_head(h_zone).squeeze(-1),
            "card_mask": self.card_mask_head(h_zone).squeeze(-1),
        }

    def decode_by_spans(self, h_next_tokens, spans):
        """
        h_next_tokens: [B, L, D]
        spans: encoder 返回的 token 区间
        """
        pred = {}

        # global_state class logits: [B, G, num_stat_classes]
        s, e = spans["global_state"]
        h_global = h_next_tokens[:, s:e]
        pred["global_state"] = self.global_head(h_global)

        # card zones
        pred["card_zones"] = {}

        for zone_name in [
            "hand",
            "library",
            "graveyard",
            "stack_cards",
        ]:
            s, e = spans[zone_name]
            h_zone = h_next_tokens[:, s:e]
            pred["card_zones"][zone_name] = self.decode_card_zone(h_zone)

        # board zones
        pred["board_zones"] = {}

        for zone_name in [
            "self_board",
            "oppo_board",
        ]:
            s, e = spans[zone_name]
            h_zone = h_next_tokens[:, s:e]
            pred["board_zones"][zone_name] = self.decode_board_zone(h_zone)

        

        return pred

    def forward(
        self,
        state_tokens,
        state_padding_mask,
        spans,
        transition_vec,
    ):
        """
        state_tokens:
            [B, L, D]

        state_padding_mask:
            [B, L]
            True = padding

        spans:
            dict

        transition_vec:
            [B, transition_dim]

        return:
            pred_next_state nested dict
        """
        transition_token = self.make_transition_memory(
            transition_vec
        )  # [B, M, D]

        h = self.decoder(
            tgt=state_tokens,
            memory=transition_token,

            # state token padding
            tgt_key_padding_mask=state_padding_mask,

        )

        h = self.final_norm(h)

        

        pred_next_state = self.decode_by_spans(
            h_next_tokens=h,
            spans=spans,
        )

        return pred_next_state




def make_fake_card_zone(
    B,
    N,
    special_type_dim,
    num_card_types,
    device,
    with_card_types=True,
    with_card_costs=True,
):
    """
    构造一个假的 card zone。

    普通 zone:
        hand / library / graveyard / stack_cards
        有 card_types / card_costs

    board zone:
        self_board / oppo_board
        你当前代码里没有 card_types / card_costs，所以可以关掉。
    """
    zone = {
        "card_special_types": torch.randint(
            0,
            2,
            (B, N, special_type_dim),
            device=device,
        ).float(),

        "card_atks": torch.randn(
            B,
            N,
            device=device,
        ),

        "card_hps": torch.randn(
            B,
            N,
            device=device,
        ),

        "card_has_state": torch.randint(
            0,
            2,
            (B, N),
            device=device,
        ).float(),

        "card_mask": (
            torch.rand(B, N, device=device) > 0.25
        ).float(),
    }

    if with_card_types:
        zone["card_types"] = torch.randint(
            0,
            num_card_types + 1,
            (B, N),
            device=device,
        )

    if with_card_costs:
        zone["card_costs"] = torch.rand(
            B,
            N,
            6,
            device=device,
        ) * 10.0

    return zone


def add_time_dim(x):
    """
    把 nested tensor dict 里的 tensor 从 [B, ...] 变成 [B, 1, ...]。
    用来模拟 dataset 输出的 T=1 格式。
    """
    if isinstance(x, dict):
        return {
            k: add_time_dim(v)
            for k, v in x.items()
        }

    return x.unsqueeze(1)


def make_fake_state(
    B,
    config,
    sizes,
    device,
    with_time_dim=True,
):
    special_type_dim = config["special_type_dim"]
    num_card_types = config["num_card_types"]

    player_one_hot = torch.zeros(
        B,
        config["stack_player_dim"],
        device=device,
    )

    if B >= 1:
        player_one_hot[0, 0] = 1.0  # self
    if B >= 2:
        player_one_hot[1, 1] = 1.0  # oppo
    # B >= 3 的第三个样本保持 [0, 0]，表示 none

    state = {
        "global_state": torch.randn(
            B,
            8,
            device=device,
        ),

        "card_zones": {
            "hand": make_fake_card_zone(
                B,
                sizes["hand"],
                special_type_dim,
                num_card_types,
                device,
                with_card_types=True,
                with_card_costs=True,
            ),

            "library": make_fake_card_zone(
                B,
                sizes["library"],
                special_type_dim,
                num_card_types,
                device,
                with_card_types=True,
                with_card_costs=True,
            ),

            "graveyard": make_fake_card_zone(
                B,
                sizes["graveyard"],
                special_type_dim,
                num_card_types,
                device,
                with_card_types=True,
                with_card_costs=True,
            ),

            "stack_cards": make_fake_card_zone(
                B,
                sizes["stack_cards"],
                special_type_dim,
                num_card_types,
                device,
                with_card_types=True,
                with_card_costs=True,
            ),
        },

        "board_zones": {
            "self_board": make_fake_card_zone(
                B,
                sizes["self_board"],
                special_type_dim,
                num_card_types,
                device,
                with_card_types=False,
                with_card_costs=False,
            ),

            "oppo_board": make_fake_card_zone(
                B,
                sizes["oppo_board"],
                special_type_dim,
                num_card_types,
                device,
                with_card_types=False,
                with_card_costs=False,
            ),
        },

        "stack_extra": {
            "player_one_hot": player_one_hot,

            "action_number": torch.randint(
                0,
                config["stack_action_vocab_size"] + 1,
                (B,),
                device=device,
            ),
        },
    }

    if with_time_dim:
        state = add_time_dim(state)

    return state


def print_pred_shapes(pred):
    print("pred.global_state:", tuple(pred["global_state"].shape))

    for zone_name, zone in pred["card_zones"].items():
        print(
            f"pred.card_zones.{zone_name}.card_types:",
            tuple(zone["card_types"].shape),
        )
        print(
            f"pred.card_zones.{zone_name}.card_mask:",
            tuple(zone["card_mask"].shape),
        )

    for zone_name, zone in pred["board_zones"].items():
        print(
            f"pred.board_zones.{zone_name}.card_mask:",
            tuple(zone["card_mask"].shape),
        )




if __name__ == "__main__":
    torch.manual_seed(0)

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    config = {
        "num_card_types": 32,
        "num_card_costs": 6,
        "num_stat_classes": 21,
        "special_type_dim": 6,
        "stack_player_dim": 2,
        "stack_action_vocab_size": 20,

        "d_model": 64,
        "nhead": 4,
        "num_layers": 2,
        "dim_feedforward": 128,
        "dropout": 0.1,
        "transition_memory_len": 10,

        "max_slots": 64,

        # decoder 的 transition_vec 维度
        # 例如可以是 concat(action_emb, card_emb, z)
        "transition_dim": 96,
    }

    sizes = {
        "hand": 5,
        "library": 8,
        "graveyard": 6,
        "stack_cards": 3,
        "self_board": 4,
        "oppo_board": 4,
    }

    B = 3

    encoder = StateTransformerEncoder(config).to(device)
    decoder = TokenTransitionStateDecoder(config).to(device)

    encoder.eval()
    decoder.eval()

    state = make_fake_state(
        B=B,
        config=config,
        sizes=sizes,
        device=device,
        with_time_dim=True,
    )

    transition_vec = torch.randn(
        B,
        config["transition_dim"],
        device=device,
    )

    with torch.no_grad():
        state_emb, state_tokens, state_padding_mask, spans = encoder(state)

        pred_next_state = decoder(
            state_tokens=state_tokens,
            state_padding_mask=state_padding_mask,
            spans=spans,
            transition_vec=transition_vec,
        )

    expected_L = (
        1  # cls
        + 8  # global_state: life*2 + mana*6
        + sizes["hand"]
        + sizes["library"]
        + sizes["graveyard"]
        + sizes["stack_cards"]
        + sizes["self_board"]
        + sizes["oppo_board"]
    )

    print("device:", device)
    print("state_emb:", tuple(state_emb.shape))
    print(
        "state_tokens:",
        tuple(state_tokens.shape),
        "expected:",
        (B, expected_L, config["d_model"]),
    )
    print("state_padding_mask:", tuple(state_padding_mask.shape))
    print("spans:", spans)

    print_pred_shapes(pred_next_state)

    assert state_emb.shape == (
        B,
        config["d_model"],
    )

    assert state_tokens.shape == (
        B,
        expected_L,
        config["d_model"],
    )

    assert state_padding_mask.shape == (
        B,
        expected_L,
    )

    assert pred_next_state["global_state"].shape == (
        B,
        8,
        config["num_stat_classes"],
    )

    assert pred_next_state["card_zones"]["hand"]["card_types"].shape == (
        B,
        sizes["hand"],
        config["num_card_types"],
    )

    assert pred_next_state["card_zones"]["hand"]["card_costs"].shape == (
        B,
        sizes["hand"],
        config["num_card_costs"],
        config["num_stat_classes"],
    )

    assert pred_next_state["card_zones"]["library"]["card_types"].shape == (
        B,
        sizes["library"],
        config["num_card_types"],
    )

    assert pred_next_state["card_zones"]["graveyard"]["card_types"].shape == (
        B,
        sizes["graveyard"],
        config["num_card_types"],
    )

    assert pred_next_state["card_zones"]["stack_cards"]["card_types"].shape == (
        B,
        sizes["stack_cards"],
        config["num_card_types"],
    )

    assert pred_next_state["board_zones"]["self_board"]["card_mask"].shape == (
        B,
        sizes["self_board"],
    )

    assert pred_next_state["board_zones"]["oppo_board"]["card_mask"].shape == (
        B,
        sizes["oppo_board"],
    )


    print("OK: encoder + decoder forward passed")
