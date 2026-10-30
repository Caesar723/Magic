import torch
import torch.nn as nn
from game.rlearning.net.variable_deck.StateTransformer import ActionTokenAdapter, StateCandidateFusionBlock



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
        nn.init.normal_(self.stack_position_embedding.weight, std=0.02)

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
        stack_tokens=entity_tokens[:,stack_start:stack_end]+stack_position_features
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

