import torch
import torch.nn as nn

from game.rlearning.states.state_space.specific_entity import BOARD_ZONE_NAMES,CARD_ZONE_NAMES


class EntityTransitionFeatures(nn.Module):
    required_models=(
        "StateTransformerEncoder","ActionEncoder","CardStateEncoder",
        "CardFusion","TransitionPlanner","PriorEncoder"
    )
    operations={
        "card_embedding":("encode_cards",("card_embeddings",)),
        "action_embedding":("encode_actions",("planner","mean_p","std_p"))
    }

    def __init__(self,models,config):
        super().__init__()
        self.models=nn.ModuleDict(models)
        planner=config["model"]["TransitionPlanner"]
        self.num_plan_tokens=planner["num_plan_tokens"]
        self.planner_dim=planner["d_model"]
        self.q_dim=config["model"]["PriorEncoder"]["latent_dim"]
        self.zone_sizes={
            "hand":10,"library":40,"graveyard":40,"stack_cards":10,
            "self_board":10,"oppo_board":10,"self_land":20,"oppo_land":20
        }

    def encode_cards(
        self,text_embeddings,card_types,card_special_types,
        card_mana_costs,card_color_identity,card_attacks,
        card_defends,card_has_state,card_mask
    ):
        attributes=self.models["CardStateEncoder"](
            card_types,card_special_types,card_mana_costs,
            card_attacks,card_defends,card_has_state,card_color_identity
        )
        features=self.models["CardFusion"](text_embeddings,attributes)
        return features.masked_fill(~card_mask.bool().unsqueeze(-1),0.0)

    def build_state(
        self,global_state,entity_card_types,entity_card_costs,
        entity_card_color_identity,entity_card_special_types,
        entity_card_atks,entity_card_hps,entity_card_has_state,
        entity_card_is_attacker,entity_card_mask,stack_player_one_hot
    ):
        state={
            "global_state":global_state,
            "card_zones":{},"board_zones":{},
            "stack_extra":{"player_one_hot":stack_player_one_hot}
        }
        start=0
        for name in CARD_ZONE_NAMES+BOARD_ZONE_NAMES:
            end=start+self.zone_sizes[name]
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
            group="card_zones" if name in CARD_ZONE_NAMES else "board_zones"
            state[group][name]=zone
            start=end
        return state

    def encode_actions(
        self,global_state,entity_card_types,entity_card_costs,
        entity_card_color_identity,entity_card_special_types,
        entity_card_atks,entity_card_hps,entity_card_has_state,
        entity_card_is_attacker,entity_card_mask,stack_player_one_hot,
        candidate_actions,candidate_text_embeddings,candidate_card_types,
        candidate_special_types,candidate_mana_costs,candidate_color_identity,
        candidate_attacks,candidate_defends,candidate_has_state,
        candidate_has_card,candidate_mask,candidate_layout=None
    ):
        num_states,num_candidates=candidate_actions.shape
        valid=None
        if candidate_layout is None:
            mask=candidate_mask.bool() & candidate_has_card.bool() & (candidate_actions>=0)
            state_ids,candidate_ids=mask.nonzero(as_tuple=True)
        else:
            state_ids=candidate_layout["state_ids"]
            candidate_ids=candidate_layout["candidate_ids"]
            valid=candidate_layout["valid"]
        if state_ids.numel()==0:
            planner=global_state.new_zeros((num_states,num_candidates,self.num_plan_tokens,self.planner_dim))
            mean=global_state.new_zeros((num_states,num_candidates,self.q_dim))
            return planner,mean,torch.zeros_like(mean)

        state=self.build_state(
            global_state,entity_card_types,entity_card_costs,
            entity_card_color_identity,entity_card_special_types,
            entity_card_atks,entity_card_hps,entity_card_has_state,
            entity_card_is_attacker,entity_card_mask,stack_player_one_hot
        )
        h_state,tokens,padding,_=self.models["StateTransformerEncoder"](state)

        def select(value):
            value=value[state_ids,candidate_ids]
            if valid is None:
                return value
            mask=valid.view((-1,)+(1,)*(value.ndim-1))
            return value.masked_fill(~mask,0)

        h_action=self.models["ActionEncoder"](select(candidate_actions))
        h_attributes=self.models["CardStateEncoder"](
            select(candidate_card_types),select(candidate_special_types),
            select(candidate_mana_costs),select(candidate_attacks),
            select(candidate_defends),select(candidate_has_state),
            select(candidate_color_identity)
        )
        h_card=self.models["CardFusion"](select(candidate_text_embeddings),h_attributes)
        selected_state=h_state[state_ids]
        planner=self.models["TransitionPlanner"](
            h_card,h_action,selected_state,tokens[state_ids],padding[state_ids]
        )
        mean,std=self.models["PriorEncoder"](h_card,h_action,selected_state)
        indices=state_ids*num_candidates+candidate_ids

        def restore(value):
            if valid is not None:
                mask=valid.view((-1,)+(1,)*(value.ndim-1))
                value=value.masked_fill(~mask,0)
            flat=value.new_zeros((num_states*num_candidates,)+value.shape[1:])
            flat.index_add_(0,indices,value)
            return flat.view(num_states,num_candidates,*value.shape[1:])

        return restore(planner),restore(mean),restore(std)