import numpy as np
import torch

from game.rlearning.utils.baseDataset import BaseDataset
from game.rlearning.utils.data import batch_to_cuda

ACTION_CARD_ZONES=("hand","library","graveyard","stack_cards")
RL_CARD_ZONES=("hand","graveyard","stack_cards")
BOARD_ZONES=("self_board","oppo_board","self_land","oppo_land")

ENTITY_FIELDS={
    "card_ids":np.int64,
    "card_types":np.int64,
    "card_costs":np.float32,
    "card_color_identity":np.float32,
    "card_special_types":np.float32,
    "card_atks":np.float32,
    "card_hps":np.float32,
    "card_has_state":np.float32,
    "card_tapped":np.float32,
    "card_tapped_valid":np.float32,
    "card_is_attacker":np.float32,
    "card_mask":np.float32
}


def scalar_value(value):
    if torch.is_tensor(value):
        return value.detach().cpu().item()
    return np.asarray(value).item()


def nested_get(data,path):
    for key in path:
        data=data[key]
    return data


def get_candidate_slot(state,action):
    action=int(action)
    for slot,candidate in enumerate(state["candidate_actions"]):
        if int(candidate["index"])==action:
            return slot
    raise ValueError(f"action {action} is not in candidate_actions")


def process_entity_zone(zone,descriptions=None,include_base_stats=False):
    result={
        field:np.asarray(zone[field],dtype=dtype)
        for field,dtype in ENTITY_FIELDS.items()
    }

    if descriptions is not None:
        result["descriptions"]=list(descriptions)

    if include_base_stats:
        result["card_base_atks"]=np.asarray(zone["card_base_atks"],dtype=np.float32)
        result["card_base_hps"]=np.asarray(zone["card_base_hps"],dtype=np.float32)

    return result


def process_global_state(state):
    return np.concatenate([
        np.asarray(state["self_life"],dtype=np.float32).reshape(-1),
        np.asarray(state["oppo_life"],dtype=np.float32).reshape(-1),
        np.asarray(state["self_mana"],dtype=np.float32).reshape(-1)
    ]).astype(np.float32)


def process_stack_extra(state):
    return {
        "player_one_hot":np.asarray(state["stack_extra"]["player_one_hot"],dtype=np.float32),
        "action_number":np.asarray(state["stack_extra"]["action_number"],dtype=np.int64)
    }


def process_action_embedding_state(state):
    return {
        "global_state":process_global_state(state),
        "card_zones":{
            zone_name:process_entity_zone(state["card_zones"][zone_name])
            for zone_name in ACTION_CARD_ZONES
        },
        "board_zones":{
            zone_name:process_entity_zone(state["board_zones"][zone_name])
            for zone_name in BOARD_ZONES
        },
        "stack_extra":process_stack_extra(state)
    }


def process_rl_state(state):
    action_state=state["action_embedding_state"]

    return {
        "global_scalars":process_global_state(state),
        "card_zones":{
            zone_name:process_entity_zone(
                state["card_zones"][zone_name],
                descriptions=action_state["card_zones"][zone_name]["card_descriptions"],
                include_base_stats=True
            )
            for zone_name in RL_CARD_ZONES
        },
        "board_zones":{
            zone_name:process_entity_zone(
                state["board_zones"][zone_name],
                descriptions=action_state["board_zones"][zone_name]["card_descriptions"],
                include_base_stats=True
            )
            for zone_name in BOARD_ZONES
        },
        "stack_extra":process_stack_extra(state)
    }


def process_candidates(candidates):
    count=len(candidates)
    result={
        "indices":np.full(count,-1,dtype=np.int64),
        "actions":np.full(count,-1,dtype=np.int64),
        "card_types":np.zeros(count,dtype=np.int64),
        "special_types":np.zeros((count,20),dtype=np.float32),
        "mana_costs":np.zeros((count,6),dtype=np.float32),
        "color_identity":np.zeros((count,5),dtype=np.float32),
        "attacks":np.zeros(count,dtype=np.float32),
        "defends":np.zeros(count,dtype=np.float32),
        "has_state":np.zeros(count,dtype=np.float32),
        "has_card":np.zeros(count,dtype=np.bool_),
        "mask":np.ones(count,dtype=np.bool_),
        "descriptions":[""]*count
    }

    for index,candidate in enumerate(candidates):
        result["indices"][index]=candidate["index"]
        if candidate["action"] is not None:
            result["actions"][index]=candidate["action"]

        card=candidate["card_info"]
        if card is None:
            continue

        result["has_card"][index]=True
        result["descriptions"][index]=card["description"]
        result["card_types"][index]=card["card_type"]
        result["special_types"][index]=card["special_type"]
        result["mana_costs"][index]=card["mana_cost"]
        result["color_identity"][index]=card["color_identity"]
        result["attacks"][index]=card["attack"]
        result["defends"][index]=card["defend"]
        result["has_state"][index]=card["has_state"]

    return result


def process_frame(state):
    return {
        "rl_state":process_rl_state(state),
        "action_embedding_state":process_action_embedding_state(
            state["action_embedding_state"]
        ),
        "candidates":process_candidates(state["candidate_actions"])
    }


def build_sequence(state,max_seq_len,planner_dim,q_dim):
    history=[
        item for item in state.get("history",[])
        if isinstance(item,dict)
    ]
    current_state={
        key:value
        for key,value in state.items()
        if key not in ("history","sequence")
    }

    if len(history)>=max_seq_len:
        records=history[-max_seq_len:]
        raw_frames=[record["state"] for record in records[1:]]+[current_state]
        action_records=records
    else:
        records=history[-(max_seq_len-1):] if max_seq_len>1 else []
        raw_frames=[record["state"] for record in records]+[current_state]
        action_records=[None]+records

    frames=[process_frame(frame) for frame in raw_frames]
    length=len(frames)

    planner=np.zeros((length,4,planner_dim),dtype=np.float32)
    mean_q=np.zeros((length,q_dim),dtype=np.float32)
    std_q=np.zeros((length,q_dim),dtype=np.float32)
    six_available=np.zeros(length,dtype=np.bool_)

    for index,record in enumerate(action_records):
        if record is None:
            continue
        planner[index]=record["planner"]
        mean_q[index]=record["mean_q"]
        std_q[index]=record["std_q"]
        six_available[index]=True

    return {
        "frames":frames,
        "planner":planner,
        "mean_q":mean_q,
        "std_q":std_q,
        "six_available":six_available,
        "length":length
    }


def pad_nested_frames(sequences,state_key,time_steps):
    batch_size=len(sequences)
    template=sequences[0]["frames"][0][state_key]

    def pad_value(value,path):
        if isinstance(value,dict):
            return {
                key:pad_value(item,path+(key,))
                for key,item in value.items()
            }

        if isinstance(value,list):
            slot_count=len(value)
            result=[
                [[""]*slot_count for _ in range(time_steps)]
                for _ in range(batch_size)
            ]

            for batch_index,sequence in enumerate(sequences):
                for time_index,frame in enumerate(sequence["frames"]):
                    current=nested_get(frame[state_key],path)
                    result[batch_index][time_index][:len(current)]=current

            return result

        value=np.asarray(value)
        result=np.zeros((batch_size,time_steps)+value.shape,dtype=value.dtype)

        for batch_index,sequence in enumerate(sequences):
            for time_index,frame in enumerate(sequence["frames"]):
                result[batch_index,time_index]=nested_get(frame[state_key],path)

        return torch.from_numpy(result)

    return pad_value(template,())


def pad_candidates(sequences,time_steps):
    batch_size=len(sequences)
    max_candidates=max(
        len(frame["candidates"]["indices"])
        for sequence in sequences
        for frame in sequence["frames"]
    )
    if max_candidates<1:
        raise ValueError("Every valid timestep must have at least one candidate")

    first=sequences[0]["frames"][0]["candidates"]
    tensor_fields=(
        "indices","actions","card_types","special_types","mana_costs",
        "color_identity","attacks","defends","has_state","has_card","mask"
    )
    result={}

    for field in tensor_fields:
        value=np.asarray(first[field])
        fill_value=-1 if field in ("indices","actions") else 0
        output=np.full(
            (batch_size,time_steps,max_candidates)+value.shape[1:],
            fill_value,
            dtype=value.dtype
        )

        for batch_index,sequence in enumerate(sequences):
            for time_index,frame in enumerate(sequence["frames"]):
                current=frame["candidates"][field]
                output[batch_index,time_index,:len(current)]=current

        result[field]=torch.from_numpy(output)

    descriptions=[
        [[""]*max_candidates for _ in range(time_steps)]
        for _ in range(batch_size)
    ]

    for batch_index,sequence in enumerate(sequences):
        for time_index,frame in enumerate(sequence["frames"]):
            current=frame["candidates"]["descriptions"]
            descriptions[batch_index][time_index][:len(current)]=current

    result["descriptions"]=descriptions
    return result


def pad_temporal(sequences):
    batch_size=len(sequences)
    time_steps=max(item["length"] for item in sequences)
    planner_dim=sequences[0]["planner"].shape[-1]
    q_dim=sequences[0]["mean_q"].shape[-1]

    planner=np.zeros((batch_size,time_steps,4,planner_dim),dtype=np.float32)
    mean_q=np.zeros((batch_size,time_steps,q_dim),dtype=np.float32)
    std_q=np.zeros((batch_size,time_steps,q_dim),dtype=np.float32)
    six_available=np.zeros((batch_size,time_steps),dtype=np.bool_)
    lengths=np.asarray([item["length"] for item in sequences],dtype=np.int64)

    for batch_index,item in enumerate(sequences):
        length=item["length"]
        planner[batch_index,:length]=item["planner"]
        mean_q[batch_index,:length]=item["mean_q"]
        std_q[batch_index,:length]=item["std_q"]
        six_available[batch_index,:length]=item["six_available"]

    return {
        "rl_state":pad_nested_frames(sequences,"rl_state",time_steps),
        "action_embedding_state":pad_nested_frames(
            sequences,
            "action_embedding_state",
            time_steps
        ),
        "candidates":pad_candidates(sequences,time_steps),
        "planner":torch.from_numpy(planner),
        "mean_q":torch.from_numpy(mean_q),
        "std_q":torch.from_numpy(std_q),
        "six_available":torch.from_numpy(six_available),
        "lengths":torch.from_numpy(lengths)
    }

class PPOAgentDataset(BaseDataset):
    def __init__(self,config):
        super().__init__(config)
        self.max_seq_len=config["max_seq_len"]
        self.planner_dim=config["planner_dim"]
        self.q_dim=config["q_dim"]

        if self.max_seq_len<1:
            raise ValueError("max_seq_len must be at least 1")

    def normalize_advantage(self,advantage):
        return (advantage-advantage.mean())/(advantage.std(unbiased=False)+1e-5)

    def calculate_advantage(self,delta,done):
        gamma=self.config["ppo"]["gamma"]
        lambd=self.config["ppo"]["lambd"]
        advantage=torch.zeros_like(delta)
        current=torch.zeros((),dtype=delta.dtype,device=delta.device)

        for index in range(len(delta)-1,-1,-1):
            current=delta[index]+gamma*lambd*(1.0-done[index])*current
            advantage[index]=current

        return advantage

    def get_sample(self,state):
        state["sequence"]=build_sequence(
            state,
            self.max_seq_len,
            self.planner_dim,
            self.q_dim
        )
        return state

    def select_states(self,batch,extra_keys):
        states=batch
        for key in extra_keys:
            states=[item[key] for item in states]
        return states

    def collate_state(self,batch,extra_keys=None):
        extra_keys=extra_keys or []
        states=self.select_states(batch,extra_keys)

        for state in states:
            if "sequence" not in state:
                self.get_sample(state)

        sequences=[state["sequence"] for state in states]
        return pad_temporal(sequences)

    @torch.no_grad()
    def data_preprocess(self,trainer):
        actions=torch.tensor(
            [int(item["action"]) for item in self.datas],
            dtype=torch.long
        )
        candidate_slots=torch.tensor([
            get_candidate_slot(item["state"],item["action"])
            for item in self.datas
        ],dtype=torch.long)
        rewards=torch.tensor([
            scalar_value(item["reward"])
            for item in self.datas
        ],dtype=torch.float32)
        done=torch.tensor([
            scalar_value(item["done"])
            for item in self.datas
        ],dtype=torch.float32)

        state_result=trainer.choose_action(self.datas,["state"])
        next_state_result=trainer.choose_action(self.datas,["next_state"])

        device=state_result["value"].device
        actions=actions.to(device)
        candidate_slots=candidate_slots.to(device)
        rewards=rewards.to(device)
        done=done.to(device)

        values=state_result["value"]
        next_values=next_state_result["value"]
        delta=(
            rewards
            +self.config["ppo"]["gamma"]*next_values*(1.0-done)
            -values
        )

        advantage=self.calculate_advantage(delta,done)
        value_target=advantage+values
        advantage=self.normalize_advantage(advantage)

        clip_value=self.config["ppo"].get("clip_value_advantage",50.0)
        advantage=advantage.clamp(-clip_value,clip_value)
        old_prob_log=state_result["dist"].log_prob(candidate_slots)

        actions=actions.cpu()
        candidate_slots=candidate_slots.cpu()
        advantage=advantage.cpu()
        value_target=value_target.cpu()
        old_prob_log=old_prob_log.cpu()

        for index,item in enumerate(self.datas):
            item["environment_action"]=actions[index]
            item["candidate_slot"]=candidate_slots[index]
            item["advantage"]=advantage[index]
            item["value_target"]=value_target[index]
            item["old_prob_log"]=old_prob_log[index]

        return self.datas

    def collate_fn(self,batch):
        result=self.collate_state(batch,["state"])

        if "candidate_slot" not in batch[0]:
            return result

        result.update({
            "action":torch.tensor([
                scalar_value(item["candidate_slot"])
                for item in batch
            ],dtype=torch.long),
            "environment_action":torch.tensor([
                scalar_value(item["environment_action"])
                for item in batch
            ],dtype=torch.long),
            "advantage":torch.tensor([
                scalar_value(item["advantage"])
                for item in batch
            ],dtype=torch.float32),
            "value_target":torch.tensor([
                scalar_value(item["value_target"])
                for item in batch
            ],dtype=torch.float32),
            "old_prob_log":torch.tensor([
                scalar_value(item["old_prob_log"])
                for item in batch
            ],dtype=torch.float32)
        })
        return result