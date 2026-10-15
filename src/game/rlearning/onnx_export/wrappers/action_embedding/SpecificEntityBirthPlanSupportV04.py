import torch

from game.rlearning.onnx_export.base import ONNXExportWrapper
from game.rlearning.states.state_space.specific_entity import BOARD_ZONE_NAMES,CARD_ZONE_NAMES


class PriorActionEmbedderWrapper(ONNXExportWrapper):
    input_names=(
        "global_state",
        "entity_card_types",
        "entity_card_costs",
        "entity_card_color_identity",
        "entity_card_special_types",
        "entity_card_atks",
        "entity_card_hps",
        "entity_card_has_state",
        "entity_card_is_attacker",
        "entity_card_mask",
        "stack_player_one_hot",
        "candidate_actions",
        "candidate_text_embeddings",
        "candidate_card_types",
        "candidate_special_types",
        "candidate_mana_costs",
        "candidate_color_identity",
        "candidate_attacks",
        "candidate_defends",
        "candidate_has_state",
        "candidate_has_card",
        "candidate_mask"
    )
    output_names=("planner","mean_p","std_p")

    zone_sizes={
        "hand":10,
        "library":40,
        "graveyard":40,
        "stack_cards":10,
        "self_board":10,
        "oppo_board":10,
        "self_land":20,
        "oppo_land":20
    }

    def __init__(self,models,training_config,export_config):
        super().__init__(models,training_config,export_config)
        required=(
            "StateTransformerEncoder","ActionEncoder","CardStateEncoder",
            "CardFusion","TransitionPlanner","PriorEncoder"
        )
        missing=[name for name in required if name not in self.models]
        if missing:
            raise KeyError(f"PriorActionEmbedderWrapper missing models: {missing}")

    def build_state(
        self,global_state,entity_card_types,entity_card_costs,
        entity_card_color_identity,entity_card_special_types,
        entity_card_atks,entity_card_hps,entity_card_has_state,
        entity_card_is_attacker,entity_card_mask,stack_player_one_hot
    ):
        state={
            "global_state":global_state,
            "card_zones":{},
            "board_zones":{},
            "stack_extra":{"player_one_hot":stack_player_one_hot}
        }
        start=0
        for zone_name in CARD_ZONE_NAMES+BOARD_ZONE_NAMES:
            end=start+self.zone_sizes[zone_name]
            zone={
                "card_types":entity_card_types[:,start:end],
                "card_costs":entity_card_costs[:,start:end],
                "card_color_identity":entity_card_color_identity[:,start:end],
                "card_special_types":entity_card_special_types[:,start:end],
                "card_atks":entity_card_atks[:,start:end],
                "card_hps":entity_card_hps[:,start:end],
                "card_has_state":entity_card_has_state[:,start:end],
                "card_is_attacker":entity_card_is_attacker[:,start:end],
                "card_mask":entity_card_mask[:,start:end]
            }
            collection="card_zones" if zone_name in CARD_ZONE_NAMES else "board_zones"
            state[collection][zone_name]=zone
            start=end
        return state

    def forward(
        self,global_state,entity_card_types,entity_card_costs,
        entity_card_color_identity,entity_card_special_types,
        entity_card_atks,entity_card_hps,entity_card_has_state,
        entity_card_is_attacker,entity_card_mask,stack_player_one_hot,
        candidate_actions,candidate_text_embeddings,candidate_card_types,
        candidate_special_types,candidate_mana_costs,candidate_color_identity,
        candidate_attacks,candidate_defends,candidate_has_state,
        candidate_has_card,candidate_mask
    ):
        state=self.build_state(
            global_state,entity_card_types,entity_card_costs,
            entity_card_color_identity,entity_card_special_types,
            entity_card_atks,entity_card_hps,entity_card_has_state,
            entity_card_is_attacker,entity_card_mask,stack_player_one_hot
        )
        h_state,state_tokens,state_padding_mask,_=self.models["StateTransformerEncoder"](state)

        num_states,num_candidates=candidate_actions.shape
        flat_count=num_states*num_candidates
        safe_actions=candidate_actions.clamp(min=0)

        h_action=self.models["ActionEncoder"](safe_actions.reshape(flat_count))
        h_card_attr=self.models["CardStateEncoder"](
            candidate_card_types.reshape(flat_count),
            candidate_special_types.reshape(flat_count,candidate_special_types.shape[-1]),
            candidate_mana_costs.reshape(flat_count,candidate_mana_costs.shape[-1]),
            candidate_attacks.reshape(flat_count),
            candidate_defends.reshape(flat_count),
            candidate_has_state.reshape(flat_count),
            candidate_color_identity.reshape(flat_count,candidate_color_identity.shape[-1])
        )
        h_text=candidate_text_embeddings.reshape(flat_count,candidate_text_embeddings.shape[-1])
        h_card=self.models["CardFusion"](h_text,h_card_attr)

        hidden_dim=h_state.shape[-1]
        token_count=state_tokens.shape[1]
        h_state=h_state.unsqueeze(1).expand(-1,num_candidates,-1).reshape(flat_count,hidden_dim)
        state_tokens=state_tokens.unsqueeze(1).expand(-1,num_candidates,-1,-1)
        state_tokens=state_tokens.reshape(flat_count,token_count,hidden_dim)
        state_padding_mask=state_padding_mask.unsqueeze(1).expand(-1,num_candidates,-1)
        state_padding_mask=state_padding_mask.reshape(flat_count,token_count)

        planner=self.models["TransitionPlanner"](
            h_card,h_action,h_state,state_tokens,state_padding_mask
        )
        mean_p,std_p=self.models["PriorEncoder"](h_card,h_action,h_state)

        planner=planner.reshape(num_states,num_candidates,planner.shape[-2],planner.shape[-1])
        mean_p=mean_p.reshape(num_states,num_candidates,mean_p.shape[-1])
        std_p=std_p.reshape(num_states,num_candidates,std_p.shape[-1])

        encoded_mask=(candidate_mask.bool()&candidate_has_card.bool()&(candidate_actions>=0))
        planner=planner.masked_fill(~encoded_mask.unsqueeze(-1).unsqueeze(-1),0.0)
        mean_p=mean_p.masked_fill(~encoded_mask.unsqueeze(-1),0.0)
        std_p=std_p.masked_fill(~encoded_mask.unsqueeze(-1),0.0)
        return planner,mean_p,std_p

    def build_example_inputs(self):
        num_states=2
        num_candidates=3
        num_entities=sum(self.zone_sizes.values())
        state_config=self.training_config["model"]["StateTransformerEncoder"]
        card_config=self.training_config["model"]["CardStateEncoder"]
        fusion_config=self.training_config["model"]["CardFusion"]
        special_dim=state_config["special_type_dim"]
        candidate_special_dim=card_config["num_special"]
        text_dim=fusion_config["text_dim"]

        global_state=torch.zeros(num_states,8,dtype=torch.float32)
        entity_card_types=torch.zeros(num_states,num_entities,dtype=torch.long)
        entity_card_costs=torch.zeros(num_states,num_entities,6,dtype=torch.float32)
        entity_card_color_identity=torch.zeros(num_states,num_entities,5,dtype=torch.float32)
        entity_card_special_types=torch.zeros(num_states,num_entities,special_dim,dtype=torch.float32)
        entity_card_atks=torch.zeros(num_states,num_entities,dtype=torch.float32)
        entity_card_hps=torch.zeros(num_states,num_entities,dtype=torch.float32)
        entity_card_has_state=torch.zeros(num_states,num_entities,dtype=torch.float32)
        entity_card_is_attacker=torch.zeros(num_states,num_entities,dtype=torch.float32)
        entity_card_mask=torch.zeros(num_states,num_entities,dtype=torch.bool)
        stack_player_one_hot=torch.zeros(num_states,self.zone_sizes["stack_cards"],2,dtype=torch.float32)

        start=0
        for size in self.zone_sizes.values():
            entity_card_mask[:,start]=True
            start+=size

        candidate_actions=torch.tensor([[0,3,-1],[1,4,2]],dtype=torch.long)
        candidate_text_embeddings=torch.zeros(num_states,num_candidates,text_dim,dtype=torch.float32)
        candidate_card_types=torch.zeros(num_states,num_candidates,dtype=torch.long)
        candidate_special_types=torch.zeros(num_states,num_candidates,candidate_special_dim,dtype=torch.float32)
        candidate_mana_costs=torch.zeros(num_states,num_candidates,6,dtype=torch.float32)
        candidate_color_identity=torch.zeros(num_states,num_candidates,5,dtype=torch.float32)
        candidate_attacks=torch.zeros(num_states,num_candidates,dtype=torch.float32)
        candidate_defends=torch.zeros(num_states,num_candidates,dtype=torch.float32)
        candidate_has_state=torch.zeros(num_states,num_candidates,dtype=torch.float32)
        candidate_has_card=torch.tensor([[True,True,False],[True,True,True]],dtype=torch.bool)
        candidate_mask=torch.tensor([[True,True,False],[True,True,True]],dtype=torch.bool)

        return (
            global_state,entity_card_types,entity_card_costs,
            entity_card_color_identity,entity_card_special_types,
            entity_card_atks,entity_card_hps,entity_card_has_state,
            entity_card_is_attacker,entity_card_mask,stack_player_one_hot,
            candidate_actions,candidate_text_embeddings,candidate_card_types,
            candidate_special_types,candidate_mana_costs,candidate_color_identity,
            candidate_attacks,candidate_defends,candidate_has_state,
            candidate_has_card,candidate_mask
        )

    def get_dynamic_axes(self,dynamic_batch=True,dynamic_candidates=True):
        axes={}
        candidate_inputs=self.input_names[11:]

        if dynamic_batch:
            for name in self.input_names+self.output_names:
                axes.setdefault(name,{})[0]="num_states"
        if dynamic_candidates:
            for name in candidate_inputs+self.output_names:
                axes.setdefault(name,{})[1]="num_candidates"
        return axes
