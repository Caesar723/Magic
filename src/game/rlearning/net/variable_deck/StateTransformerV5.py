import torch
import torch.nn as nn

from game.rlearning.net.variable_deck.StateTransformerV4 import StateTransformer as StateTransformerV4


class StateTransformer(StateTransformerV4):
    def __init__(self, config):
        super().__init__(config)

        self.kind_to_id = {"cls": 0, "action": 1, "scalar": 2, "card": 3, "board_card": 4, "candidate": 5}
        self.owner_to_id = {"none": 0, "self": 1, "oppo": 2}

        zone_layout = (
            ("hand", 10, "self", "card"),
            ("graveyard", 40, "self", "card"),
            ("stack_cards", 10, "none", "card"),
            ("self_board", 10, "self", "board_card"),
            ("oppo_board", 10, "oppo", "board_card"),
            ("self_land", 20, "self", "board_card"),
            ("oppo_land", 20, "oppo", "board_card"),
        )

        self.zone_to_id = {name: i for i, (name, _, _, _) in enumerate(zone_layout)}



        zone_ids, owner_ids, kind_ids = [], [], []

        for name, size, owner, kind in zone_layout:
            zone_ids.extend([self.zone_to_id[name]] * size)
            owner_ids.extend([self.owner_to_id[owner]] * size)
            kind_ids.extend([self.kind_to_id[kind]] * size)
            
        for name, ids in (
            ("entity_zone_ids", zone_ids),
            ("entity_owner_ids", owner_ids),
            ("entity_kind_ids", kind_ids),
        ):
            self.register_buffer(
                name,
                torch.tensor(ids, dtype=torch.long),
                persistent=False,
            )

        self.zone_embedding = nn.Embedding(len(self.zone_to_id), self.embed_dim)
        self.kind_embedding = nn.Embedding(len(self.kind_to_id), self.embed_dim)
        
        nn.init.normal_(self.zone_embedding.weight, std=0.02)
        nn.init.normal_(self.kind_embedding.weight, std=0.02)

    def _kind(self, name):
        return self.kind_embedding.weight[self.kind_to_id[name]]

    def _encode_entities(
        self, entities, entity_mask,stack_owner_ids
    ):
        stack_start = self.stack_start
        stack_end = stack_start + self.max_stack_size
        num_valid = entities.shape[0]

        owner_ids = self.entity_owner_ids.unsqueeze(0).expand(num_valid, -1)
        owner_ids = torch.cat(
            [
                owner_ids[:, :stack_start],
                stack_owner_ids,
                owner_ids[:, stack_end:],
            ],
            dim=1,
        )


        entities = entities.masked_fill(~entity_mask.unsqueeze(-1), 0.0)

        tokens=(
            self.entity_proj(entities)
            + self.zone_embedding(self.entity_zone_ids).unsqueeze(0)
            + self.stack_owner_embedding(owner_ids)
            + self.kind_embedding(self.entity_kind_ids).unsqueeze(0)
        )
        

        positions=torch.arange(self.max_stack_size, device=entities.device)

        stack_tokens=tokens[:, stack_start:stack_end]+ self.stack_position_embedding(positions).unsqueeze(0)

        tokens = torch.cat(
            [tokens[:, :stack_start], stack_tokens, tokens[:, stack_end:]],
            dim=1,
        )
        tokens = self.entity_norm(tokens)
        return tokens.masked_fill(~entity_mask.unsqueeze(-1), 0.0)






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
        num_valid = scalars.shape[0]

        cls=self.cls_token.expand(num_valid, -1, -1)+self._kind("cls")
        cls_mask = torch.ones(num_valid, 1, dtype=torch.bool, device=device)

        action_tokens, action_mask = self.action_token_adapter(planner, mean_p, std_p, action_available, special_action_ids)
        action_tokens = (action_tokens+self._kind("action")).masked_fill(~action_mask.unsqueeze(-1), 0.0)

        scalar_tokens = self.scalar_norm(
            self.scalar_proj(scalars.unsqueeze(-1)) 
            + self.scalar_slots
            + self._kind("scalar")
        )
        scalar_mask = torch.ones(
            num_valid, self.num_scalars,
            dtype=torch.bool, device=device,
        )

        entity_tokens = self._encode_entities(entities,entity_mask_valid,owner_id)


        candidates = candidates.masked_fill(~candidate_mask_valid.unsqueeze(-1), 0.0)
        candidate_tokens = self.candidate_norm(self.candidate_proj(candidates)+ self._kind("candidate"))
        candidate_tokens = candidate_tokens.masked_fill(~candidate_mask_valid.unsqueeze(-1), 0.0)

        stack_start = self.stack_start
        stack_end = stack_start + self.max_stack_size


        card_stack_relation = self.build_stack_relation(
            stack_action,
            owner_id,
            entity_mask_valid[:, stack_start:stack_end],
            num_entities,
        ).to(dtype=entity_tokens.dtype)
        heads = self.stack_relation_beta.shape[0]
        bias = self.stack_relation_beta.view(1, heads, 1, 1) * card_stack_relation[:, None]
        attn_mask = bias.reshape(num_valid * heads, card_stack_relation.shape[-1], card_stack_relation.shape[-1])

        state_tokens = torch.cat(
            [cls, action_tokens, scalar_tokens, entity_tokens],dim=1,
        )
        state_mask = torch.cat(
            [cls_mask, action_mask, scalar_mask, entity_mask_valid], dim=1
        )

        fused_tokens = self.state_candidate_fusion_block(
            state_tokens,
            candidate_tokens,
            token_mask=state_mask,
            candidate_mask=candidate_mask_valid,
            attn_mask=attn_mask,
        )
        fused_tokens = self.output_norm(fused_tokens)
        fused_tokens = fused_tokens.masked_fill(~state_mask.unsqueeze(-1), 0.0)
        
        # combine cls, action, stack top
        cls = fused_tokens[:, 0]
        action = self.action_pool(fused_tokens[:, 1:7].flatten(1))
        action = action * action_mask[:, :1].to(action.dtype)
        entity_offset = 1 + 6 + self.num_scalars
        stack = fused_tokens[:, entity_offset + stack_start:entity_offset + stack_end]
        stack_mask = entity_mask_valid[:, stack_start:stack_end]
        slot = torch.arange(self.max_stack_size, device=device)
        top_index = (stack_mask.long() * slot).argmax(dim=1)
        rows = torch.arange(num_valid, device=device)
        top = stack[rows, top_index]* stack_mask.any(dim=1, keepdim=True).to(stack.dtype)
        valid_features = torch.cat([cls, action, top], dim=-1)



        flat_features = valid_features.new_zeros(batch_size * time_steps,valid_features.shape[-1])
        flat_features = flat_features.index_copy(0, valid_indices, valid_features)

        state_features = flat_features.view(batch_size, time_steps, -1)

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
