import torch
import torch.nn as nn
from game.rlearning.net.variable_deck.StateTransformer import ActionTokenAdapter


class FusionLayer(nn.Module):

    def __init__(self,config):
        super().__init__()
        self.config = config

        self.embed_dim = config["embed_dim"]
        self.num_heads = config.get("num_heads", 4)
        self.ffn_dim = config.get(
            "ffn_dim", self.embed_dim * 4
        )
        self.dropout_rate = config.get("dropout", 0.1)
        self.activation = config.get("activation", "gelu")

        self.self_attn = nn.MultiheadAttention(
            embed_dim=self.embed_dim,
            num_heads=self.num_heads,
            dropout=self.dropout_rate,
            batch_first=True
        )

        self.cross_attn = nn.MultiheadAttention(
            embed_dim=self.embed_dim,
            num_heads=self.num_heads,
            dropout=self.dropout_rate,
            batch_first=True
        )

        activation = {"relu": nn.ReLU,"gelu": nn.GELU,"silu": nn.SiLU}[self.activation.lower()]()

        self.ffn = nn.Sequential(
            nn.Linear(self.embed_dim, self.ffn_dim),
            activation,
            nn.Dropout(self.dropout_rate),
            nn.Linear(self.ffn_dim, self.embed_dim)
        )

        self.norm1 = nn.LayerNorm(self.embed_dim)
        self.norm2 = nn.LayerNorm(self.embed_dim)
        self.norm3 = nn.LayerNorm(self.embed_dim)

        self.dropout = nn.Dropout(self.dropout_rate)

    @staticmethod
    def mask_queries(x, valid_mask):
        if valid_mask is None:
            return x
        return x.masked_fill(~valid_mask.unsqueeze(-1), 0.0)

    def forward(self, x, c, token_mask=None, candidate_mask=None, attn_mask=None):
        token_padding_mask = ~token_mask.bool() if token_mask is not None else None
        candidate_padding_mask = ~candidate_mask.bool() if candidate_mask is not None else None

        # 1. Self-Attention
        x = self.mask_queries(x, token_mask)
        y = self.norm1(x)
        attn_out, _=self.self_attn(y,y,y,key_padding_mask=token_padding_mask,attn_mask=attn_mask,need_weights=False)
        x = self.mask_queries(x + self.dropout(attn_out), token_mask)

        # 2. Cross-Attention
        y = self.norm2(x)
        attn_out, _=self.cross_attn(y,c,c,key_padding_mask=candidate_padding_mask,need_weights=False)
        x = self.mask_queries(x + self.dropout(attn_out), token_mask)

        # 3. FFN
        y = self.ffn(self.norm3(x))
        x = self.mask_queries(x + self.dropout(y), token_mask)
        return x

class StateCandidateFusionBlock(nn.Module):
    def __init__(self, config):
        super().__init__()

        self.config = config
        self.num_layers = config.get("num_layers", 2)

        self.layers = nn.ModuleList([
            FusionLayer(config)
            for _ in range(self.num_layers)
        ])


    def forward(self,x,candidates,token_mask=None,candidate_mask=None, attn_mask=None):
        for layer in self.layers:
            x = layer(x,candidates,token_mask,candidate_mask, attn_mask)

        return x

class StateTransformer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        d = config["embed_dim"]

        self.embed_dim = d
        self.num_scalars = config["num_scalars"]
        self.max_seq_len = config["max_seq_len"]
        self.candidate_dim = config["candidate_dim"]
        self.entity_dim = config["entity_dim"]

        self.cls_token = nn.Parameter(torch.randn(1, 1, self.embed_dim) * 0.02)


        self.scalar_proj = nn.Linear(1, d)
        self.scalar_slots = nn.Parameter(torch.randn(1, self.num_scalars, d) * 0.02)
        self.scalar_norm = nn.LayerNorm(d)

        self.entity_proj = nn.Linear(self.entity_dim, d)
        self.entity_norm = nn.LayerNorm(d)

        # stack start and max stack size
        self.stack_start = config.get("stack_start", 50)
        self.max_stack_size = config.get("max_stack_size", 10)

        # stack position embedding
        self.stack_position_embedding = nn.Embedding(self.max_stack_size, d)
        self.stack_owner_embedding = nn.Embedding(3, d)
        nn.init.normal_(self.stack_position_embedding.weight, std=0.02)
        nn.init.normal_(self.stack_owner_embedding.weight, std=0.02)
        self.stack_relation_beta = nn.Parameter(torch.ones(config.get("num_heads", 4)))
        

        self.candidate_proj = nn.Linear(self.candidate_dim, d)
        self.candidate_norm = nn.LayerNorm(d)

        #Six Action Encoder Tokens
        self.action_token_adapter = ActionTokenAdapter(config)

        #Global Scalar Tokens
        self.state_candidate_fusion_block = StateCandidateFusionBlock(config)

        self.output_norm = nn.LayerNorm(d)

    @staticmethod
    def select_time(x, flat_time_mask):
        """[B, T, ...] -> [N, ...], N = sum(lengths)."""
        return x.flatten(0, 1)[flat_time_mask]

    def forward(
        self,global_scalars,entity_features,candidate_features,
        planner,mean_p,std_p,
        lengths,six_available,special_action_ids,
        stack_owner, stack_action,
        entity_mask=None,candidate_mask=None,
    ):
        batch_size, time_steps, num_scalars = global_scalars.shape
        device = global_scalars.device
        num_entities = entity_features.shape[2]
        num_candidates = candidate_features.shape[2]

        lengths = torch.as_tensor(lengths, dtype=torch.long, device=device)
        time_mask = torch.arange(time_steps, device=device)[None] < lengths[:, None]
        flat_time_mask = time_mask.reshape(-1)
        valid_indices = flat_time_mask.nonzero(as_tuple=False).squeeze(-1)

        six_available = six_available.to(device=device, dtype=torch.bool)

        if entity_mask is None:
            entity_mask = torch.ones(
                batch_size, time_steps, num_entities,
                dtype=torch.bool, device=device,
            )
        else:
            entity_mask = entity_mask.to(device=device, dtype=torch.bool)

        if candidate_mask is None:
            candidate_mask = torch.ones(
                batch_size, time_steps, num_candidates,
                dtype=torch.bool, device=device,
            )
        else:
            candidate_mask = candidate_mask.to(device=device, dtype=torch.bool)



        scalars = self.select_time(global_scalars, flat_time_mask)#[B,T,G] → [B*T,G] → [N,G]
        entities = self.select_time(entity_features, flat_time_mask)#[B,T,E,D] → [B*T,E,D] → [N,E,D]
        candidates = self.select_time(candidate_features, flat_time_mask)#[B,T,C,D] → [B*T,C,D] → [N,C,D]

        planner = self.select_time(planner, flat_time_mask)#[B,T,4,D] → [B*T,4,D] → [N,4,D]
        mean_p = self.select_time(mean_p, flat_time_mask)#[B,T,D] → [B*T,D] → [N,D]
        std_p = self.select_time(std_p, flat_time_mask)#[B,T,D] → [B*T,D] → [N,D]

        action_available = self.select_time(six_available, flat_time_mask) # [N]
        special_action_ids = self.select_time(special_action_ids, flat_time_mask) # [N]
        entity_mask_valid = self.select_time(entity_mask, flat_time_mask) # [N,E]
        candidate_mask_valid = self.select_time(candidate_mask, flat_time_mask) # [N,C]

        stack_owner = self.select_time(stack_owner, flat_time_mask).to(device=device)
        stack_action = self.select_time(stack_action, flat_time_mask).to(device=device).long()

        owner_id = torch.zeros(stack_owner.shape[:2], dtype=torch.long, device=device)
        owner_id = owner_id.masked_fill(stack_owner[..., 0] > 0.5, 1)
        owner_id = owner_id.masked_fill(stack_owner[..., 1] > 0.5, 2)

        num_valid = scalars.shape[0] #N, Number of valid time steps

        cls = self.cls_token.expand(num_valid, -1, -1)
        cls_mask = torch.ones(num_valid, 1, dtype=torch.bool, device=device)

        action_tokens, action_mask = self.action_token_adapter(planner, mean_p, std_p, action_available, special_action_ids)

        scalar_tokens = self.scalar_norm(
            self.scalar_proj(scalars.unsqueeze(-1)) 
            + self.scalar_slots
        )
        scalar_mask = torch.ones(
            num_valid, self.num_scalars,
            dtype=torch.bool, device=device,
        )

        entities = entities.masked_fill(~entity_mask_valid.unsqueeze(-1), 0.0)
        entity_tokens = self.entity_proj(entities)
        
        stack_start = self.stack_start
        stack_end = stack_start + self.max_stack_size
        stack_positions = torch.arange(self.max_stack_size,device=device)
        stack_position_features = self.stack_position_embedding(stack_positions).unsqueeze(0)
        stack_tokens=(
            entity_tokens[:,stack_start:stack_end]
            +stack_position_features
            +self.stack_owner_embedding(owner_id)
        )
        entity_tokens=torch.cat([entity_tokens[:,:stack_start],stack_tokens,entity_tokens[:,stack_end:]],dim=1)

        entity_tokens = self.entity_norm(entity_tokens)
        entity_tokens = entity_tokens.masked_fill(~entity_mask_valid.unsqueeze(-1), 0.0)


        candidates = candidates.masked_fill(~candidate_mask_valid.unsqueeze(-1), 0.0)
        candidate_tokens = self.candidate_norm(self.candidate_proj(candidates))
        candidate_tokens = candidate_tokens.masked_fill(~candidate_mask_valid.unsqueeze(-1), 0.0)


        
        state_tokens = torch.cat(
            [cls, action_tokens, scalar_tokens, entity_tokens], dim=1
        )
        state_mask = torch.cat(
            [cls_mask, action_mask, scalar_mask, entity_mask_valid], dim=1
        )

        fused_tokens = self.state_candidate_fusion_block(
            state_tokens,
            candidate_tokens,
            token_mask=state_mask,
            candidate_mask=candidate_mask_valid,
        )

        fused_tokens = self.output_norm(fused_tokens)
        fused_tokens = fused_tokens.masked_fill(~state_mask.unsqueeze(-1), 0.0)
        valid_state_features = fused_tokens[:, 0]  # [N, D]

        #return to original shape
        flat_features = valid_state_features.new_zeros(batch_size * time_steps, self.embed_dim)
        flat_features = flat_features.index_copy(0, valid_indices, valid_state_features)

        state_features = flat_features.view(batch_size, time_steps, self.embed_dim)

        flat_candidates = candidate_tokens.new_zeros(
            batch_size * time_steps,
            num_candidates,
            self.embed_dim,
        )
        flat_candidates = flat_candidates.index_copy(0, valid_indices, candidate_tokens)
        all_candidates = flat_candidates.view(batch_size, time_steps, num_candidates, self.embed_dim)

        batch_indices = torch.arange(batch_size, device=device)
        last_indices = lengths - 1

        return {
            "state_features": state_features,
            "all_candidates":all_candidates,
            "last_state_feature": state_features[batch_indices, last_indices],
            "last_candidates": all_candidates[batch_indices, last_indices],
            "last_candidate_mask": candidate_mask[batch_indices, last_indices],
            "time_mask": time_mask,
        }

    def build_stack_relation(self, action, owner_id, stack_mask, num_entities):
        action = action.clone()
        is_oppo = owner_id == 2
        swapped = action.clone()
        swapped = torch.where((action >= 6) & (action <= 15), action + 10, swapped)
        swapped = torch.where((action >= 16) & (action <= 25), action - 10, swapped)
        swapped = torch.where(action == 26, torch.full_like(action, 27), swapped)
        swapped = torch.where(action == 27, torch.full_like(action, 26), swapped)
        action = torch.where(is_oppo, swapped, action)

        entity_offset = 1 + 6 + self.num_scalars
        length = entity_offset + num_entities
        relation = action.new_zeros(action.shape[0], length, length)
        rows = torch.arange(action.shape[0], device=action.device)

        self_board = self.stack_start + self.max_stack_size
        oppo_board = self_board + 10
        self_life = 1 + 6
        oppo_life = self_life + 1

        for slot in range(self.max_stack_size):
            valid = stack_mask[:, slot]
            query = entity_offset + self.stack_start + slot
            value = action[:, slot]

            oppo_field = valid & (value >= 6) & (value <= 15)
            self_field = valid & (value >= 16) & (value <= 25)
            oppo_slot = (value - 6).clamp(0, 9)
            self_slot = (value - 16).clamp(0, 9)
            relation[rows[oppo_field], query, entity_offset + oppo_board + oppo_slot[oppo_field]] = 1
            relation[rows[self_field], query, entity_offset + self_board + self_slot[self_field]] = 1

            to_oppo = valid & (value == 26)
            to_self = valid & (value == 27)
            relation[rows[to_oppo], query, oppo_life] = 1
            relation[rows[to_self], query, self_life] = 1

        return relation