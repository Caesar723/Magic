import numpy as np


class CasterPolicyInputs:
    def __init__(self,config):
        self.planner_dim=config["planner_dim"]
        self.q_dim=config["q_dim"]
        self.actor_hidden_dim=config["model"]["TemporalBlockActor"]["hidden_dim"]
        self.critic_hidden_dim=config["model"]["TemporalBlockCritic"]["hidden_dim"]

        self.rl_card_zones=("hand","graveyard","stack_cards")
        self.action_card_zones=("hand","library","graveyard","stack_cards")
        self.board_zones=("self_board","oppo_board","self_land","oppo_land")
        self.rl_paths=self._paths(self.rl_card_zones)
        self.action_paths=self._paths(self.action_card_zones)

        self.entity_fields={
            "card_types":("card_types",np.int64),
            "card_special_types":("card_special_types",np.float32),
            "card_mana_costs":("card_costs",np.float32),
            "card_color_identity":("card_color_identity",np.float32),
            "card_attacks":("card_atks",np.float32),
            "card_defends":("card_hps",np.float32),
            "card_has_state":("card_has_state",np.float32)
        }
        self.dynamic_fields=("card_base_atks","card_base_hps","card_tapped","card_tapped_valid","card_is_attacker")
        self.action_fields=("card_types","card_costs","card_color_identity","card_special_types","card_atks","card_hps","card_has_state","card_is_attacker","card_mask")

        self.candidate_specs={
            "indices":((),np.int64,-1),
            "actions":((),np.int64,-1),
            "card_types":((),np.int64,0),
            "special_types":((20,),np.float32,0),
            "mana_costs":((6,),np.float32,0),
            "color_identity":((5,),np.float32,0),
            "attacks":((),np.float32,0),
            "defends":((),np.float32,0),
            "has_state":((),np.float32,0),
            "has_card":((),np.bool_,False),
            "mask":((),np.bool_,False)
        }
        self.candidate_fields={
            "card_types":"card_type",
            "special_types":"special_type",
            "mana_costs":"mana_cost",
            "color_identity":"color_identity",
            "attacks":"attack",
            "defends":"defend",
            "has_state":"has_state"
        }

    def _paths(self,card_zones):
        cards=tuple(("card_zones",name) for name in card_zones)
        boards=tuple(("board_zones",name) for name in self.board_zones)
        return cards+boards

    @staticmethod
    def _time_array(values,dtype):
        return np.asarray(values,dtype=dtype)[:,None]

    def _state(self,states,action=False):
        values=[state["action_embedding_state"] for state in states] if action else states
        globals_=[
            np.concatenate([
                np.asarray(state["self_life"],dtype=np.float32).reshape(-1),
                np.asarray(state["oppo_life"],dtype=np.float32).reshape(-1),
                np.asarray(state["self_mana"],dtype=np.float32).reshape(-1)
            ])
            for state in values
        ]
        name="global_state" if action else "global_scalars"
        result={name:self._time_array(globals_,np.float32)}
        fields=(("player_one_hot",np.float32),("action_number",np.int64))
        result["stack_extra"]={
            key:self._time_array([state["stack_extra"][key] for state in values],dtype)
            for key,dtype in fields
        }
        return result

    def _candidates(self,states):
        capacity=max(len(state["candidate_actions"]) for state in states)
        result={
            name:np.full((len(states),1,capacity)+shape,fill,dtype=dtype)
            for name,(shape,dtype,fill) in self.candidate_specs.items()
        }
        descriptions=[[[""]*capacity] for _ in states]

        for row,state in enumerate(states):
            for slot,candidate in enumerate(state["candidate_actions"]):
                result["indices"][row,0,slot]=candidate["index"]
                if candidate["action"] is not None:
                    result["actions"][row,0,slot]=candidate["action"]
                result["mask"][row,0,slot]=True

                card=candidate["card_info"]
                if card is None:
                    continue

                result["has_card"][row,0,slot]=True
                descriptions[row][0][slot]=card["description"]
                for name,source in self.candidate_fields.items():
                    result[name][row,0,slot]=card[source]

        result["descriptions"]=descriptions
        return result

    @staticmethod
    def _lstm(states,hidden_dim):
        hidden=[]
        cell=[]

        for state in states:
            if state is None:
                h=np.zeros((1,1,hidden_dim),dtype=np.float32)
                c=np.zeros_like(h)
            else:
                h,c=state
                h=np.asarray(h,dtype=np.float32).copy()
                c=np.asarray(c,dtype=np.float32).copy()

            hidden.append(h)
            cell.append(c)

        return {
            "h":np.concatenate(hidden,axis=1),
            "c":np.concatenate(cell,axis=1)
        }

    @staticmethod
    def _zone_field(states,paths,field,dtype):
        values=[
            np.asarray([state[group][zone][field] for state in states],dtype=dtype)
            for group,zone in paths
        ]
        return np.concatenate(values,axis=1)

    def _features(self,states):
        mask=self._zone_field(states,self.rl_paths,"card_mask",np.bool_)
        slots=np.flatnonzero(mask.reshape(-1))
        descriptions=[
            text
            for state in states
            for group,zone in self.rl_paths
            for text in state["action_embedding_state"][group][zone]["card_descriptions"]
        ]

        inputs={"card_mask":np.ones(len(slots),dtype=np.bool_)}
        for name,(field,dtype) in self.entity_fields.items():
            value=self._zone_field(states,self.rl_paths,field,dtype)
            inputs[name]=value.reshape((-1,)+value.shape[2:])[slots]

        dynamic=np.stack([
            self._zone_field(states,self.rl_paths,name,np.float32)
            for name in self.dynamic_fields
        ],axis=-1)

        action_states=[state["action_embedding_state"] for state in states]
        action_inputs={
            name:self._zone_field(
                action_states,self.action_paths,name,
                np.int64 if name=="card_types" else np.float32
            )
            for name in self.action_fields
        }

        return {
            "_packed_entities":{
                "inputs":inputs,
                "slots":slots,
                "count":len(slots),
                "descriptions":[descriptions[index] for index in slots],
                "mask":mask,
                "dynamic":dynamic
            },
            "_packed_action":action_inputs
        }

    def __call__(self,states):
        batch_size=len(states)
        planner=np.zeros((batch_size,1,4,self.planner_dim),dtype=np.float32)
        mean_p=np.zeros((batch_size,1,self.q_dim),dtype=np.float32)
        std_p=np.zeros_like(mean_p)
        available=np.zeros((batch_size,1),dtype=np.bool_)
        special_ids=np.full((batch_size,1),-1,dtype=np.int64)

        for row,state in enumerate(states):
            history=state.get("history",[])
            record=history[-1] if history and isinstance(history[-1],dict) else None
            if record is None:
                continue

            planner[row,0]=record["planner"]
            mean_p[row,0]=record["mean_p"]
            std_p[row,0]=record["std_p"]
            available[row,0]=True
            if int(record["action"]) in (0,1):
                special_ids[row,0]=int(record["action"])

        result={
            "rl_state":self._state(states),
            "action_embedding_state":self._state(states,action=True),
            "candidates":self._candidates(states),
            "planner":planner,
            "mean_p":mean_p,
            "std_p":std_p,
            "six_available":available,
            "special_action_ids":special_ids,
            "lengths":np.ones(batch_size,dtype=np.int64),
            "actor_state_in":self._lstm(
                [state["actor_state_in"] for state in states],self.actor_hidden_dim
            ),
            "critic_state_in":self._lstm(
                [state["critic_state_in"] for state in states],self.critic_hidden_dim
            )
        }
        result.update(self._features(states))
        return result