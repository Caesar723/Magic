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


def build_sequence(states,planner_dim,q_dim):
    length=len(states)
    frames=[process_frame(state) for state in states]
    planner=np.zeros((length,4,planner_dim),dtype=np.float32)
    mean_p=np.zeros((length,q_dim),dtype=np.float32)
    std_p=np.zeros((length,q_dim),dtype=np.float32)
    six_available=np.zeros(length,dtype=np.bool_)
    special_action_ids=np.full(length,-1,dtype=np.int64)

    for index,state in enumerate(states):
        history=state.get("history",[])
        record=history[-1] if history and isinstance(history[-1],dict) else None
        if record is None:
            continue

        planner[index]=record["planner"]
        mean_p[index]=record["mean_p"]
        std_p[index]=record["std_p"]
        six_available[index]=True
        if int(record["action"]) in (0,1):
            special_action_ids[index]=int(record["action"])

    return {
        "frames":frames,
        "planner":planner,
        "mean_p":mean_p,
        "std_p":std_p,
        "six_available":six_available,
        "special_action_ids":special_action_ids,
        "length":length
    }

def collate_lstm_states(states,hidden_dim):
    hidden=[]
    cell=[]

    for state in states:
        if state is None:
            h=torch.zeros((1,1,hidden_dim),dtype=torch.float32)
            c=torch.zeros_like(h)
        else:
            h,c=state
            h=torch.as_tensor(h,dtype=torch.float32).detach().cpu().clone()
            c=torch.as_tensor(c,dtype=torch.float32).detach().cpu().clone()
        hidden.append(h)
        cell.append(c)

    return {
        "h":torch.cat(hidden,dim=1),
        "c":torch.cat(cell,dim=1)
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
    q_dim=sequences[0]["mean_p"].shape[-1]

    planner=np.zeros((batch_size,time_steps,4,planner_dim),dtype=np.float32)
    mean_p=np.zeros((batch_size,time_steps,q_dim),dtype=np.float32)
    std_p=np.zeros((batch_size,time_steps,q_dim),dtype=np.float32)
    six_available=np.zeros((batch_size,time_steps),dtype=np.bool_)
    special_action_ids=np.full((batch_size,time_steps),-1,dtype=np.int64)
    lengths=np.asarray([item["length"] for item in sequences],dtype=np.int64)

    for batch_index,item in enumerate(sequences):
        length=item["length"]
        planner[batch_index,:length]=item["planner"]
        mean_p[batch_index,:length]=item["mean_p"]
        std_p[batch_index,:length]=item["std_p"]
        six_available[batch_index,:length]=item["six_available"]
        special_action_ids[batch_index,:length]=item["special_action_ids"]

    return {
        "rl_state":pad_nested_frames(sequences,"rl_state",time_steps),
        "action_embedding_state":pad_nested_frames(
            sequences,
            "action_embedding_state",
            time_steps
        ),
        "candidates":pad_candidates(sequences,time_steps),
        "planner":torch.from_numpy(planner),
        "mean_p":torch.from_numpy(mean_p),
        "std_p":torch.from_numpy(std_p),
        "six_available":torch.from_numpy(six_available),
        "special_action_ids":torch.from_numpy(special_action_ids),
        "lengths":torch.from_numpy(lengths)
    }

class PPOAgentDataset(BaseDataset):
    def __init__(self,config):
        super().__init__(config)
        self.planner_dim=config["planner_dim"]
        self.q_dim=config["q_dim"]
        self.train_seq_len=config["train_seq_len"]
        self.actor_hidden_dim=config["model"]["TemporalBlockActor"]["hidden_dim"]
        self.critic_hidden_dim=config["model"]["TemporalBlockCritic"]["hidden_dim"]
        self.segments=[]

    def __len__(self):
        return len(self.segments)

    def __getitem__(self,index):
        start,end=self.segments[index]
        items=self.datas[start:end]
        states=[item["state"] for item in items]
        record=states[0]["decision_record"]

        return {
            "sequence":build_sequence(states,self.planner_dim,self.q_dim),
            "items":items,
            "actor_state_in":record["actor_state_in"],
            "critic_state_in":record["critic_state_in"]
        }

    def is_full(self):
        return len(self.datas)>self.config.get("max_store",1000)

    def clear_data(self):
        super().clear_data()
        self.segments=[]

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
        state["sequence"]=build_sequence([state],self.planner_dim,self.q_dim)
        return state

    def select_states(self,batch,extra_keys):
        states=batch
        for key in extra_keys:
            states=[item[key] for item in states]
        return states

    def collate_state(self,batch,extra_keys=None):
        states=self.select_states(batch,extra_keys or [])

        for state in states:
            self.get_sample(state)

        result=pad_temporal([state["sequence"] for state in states])
        result["actor_state_in"]=collate_lstm_states([state["actor_state_in"] for state in states],self.actor_hidden_dim)
        result["critic_state_in"]=collate_lstm_states([state["critic_state_in"] for state in states],self.critic_hidden_dim)
        return result

    @torch.no_grad()
    def data_preprocess(self,trainer):
        actions=torch.tensor([int(item["action"]) for item in self.datas],dtype=torch.long)
        candidate_slots=torch.tensor([
            get_candidate_slot(item["state"],item["action"])
            for item in self.datas
        ],dtype=torch.long)
        rewards=torch.tensor([scalar_value(item["reward"]) for item in self.datas],dtype=torch.float32)
        done=torch.tensor([scalar_value(item["done"]) for item in self.datas],dtype=torch.float32)
        if trainer.rank==0 and done.bool().any():
            batch_extra={
                "reward":rewards,
                "done":done,
                "global_reward":[scalar_value(item["global_reward"]) for item in self.datas]
            }
            self.log_data(trainer,batch_extra)
        records=[item["state"]["decision_record"] for item in self.datas]
        values=torch.tensor([scalar_value(record["value"]) for record in records],dtype=torch.float32)
        old_prob_log=torch.tensor([scalar_value(record["sampled_log_prob"]) for record in records],dtype=torch.float32)
        next_values=torch.tensor([
            0.0 if scalar_value(item["done"]) else scalar_value(item["next_state"]["decision_record"]["value"])
            for item in self.datas
        ],dtype=torch.float32)

        delta=rewards+self.config["ppo"]["gamma"]*next_values*(1.0-done)-values
        advantage=self.calculate_advantage(delta,done)
        value_target=advantage+values
        advantage=self.normalize_advantage(advantage)

        clip_value=self.config["ppo"].get("clip_value_advantage",50.0)
        advantage=advantage.clamp(-clip_value,clip_value)

        for index,item in enumerate(self.datas):
            item["environment_action"]=actions[index]
            item["candidate_slot"]=candidate_slots[index]
            item["advantage"]=advantage[index]
            item["value_target"]=value_target[index]
            item["old_prob_log"]=old_prob_log[index]
        self.build_segments()
        return self.datas

    def build_segments(self):
        self.segments=[]
        start=0

        for index,item in enumerate(self.datas):
            end=index+1
            if scalar_value(item["done"]) or end-start>=self.train_seq_len:
                self.segments.append((start,end))
                start=end

        if start<len(self.datas):
            self.segments.append((start,len(self.datas)))

    def collate_fn(self,batch):
        result=pad_temporal([item["sequence"] for item in batch])
        batch_size=len(batch)
        time_steps=int(result["lengths"].max().item())
        lengths=result["lengths"]

        result["valid_mask"]=torch.arange(time_steps).unsqueeze(0)<lengths.unsqueeze(1)
        result["actor_state_in"]=collate_lstm_states([item["actor_state_in"] for item in batch],self.actor_hidden_dim)
        result["critic_state_in"]=collate_lstm_states([item["critic_state_in"] for item in batch],self.critic_hidden_dim)

        fields={
            "action":("candidate_slot",torch.long,0),
            "environment_action":("environment_action",torch.long,-1),
            "reward":("reward",torch.float32,0),
            "done":("done",torch.float32,0),
            "global_reward":("global_reward",torch.float32,0),
            "advantage":("advantage",torch.float32,0),
            "value_target":("value_target",torch.float32,0),
            "old_prob_log":("old_prob_log",torch.float32,0)
        }

        for target,(source,dtype,fill_value) in fields.items():
            values=torch.full((batch_size,time_steps),fill_value,dtype=dtype)
            for index,sample in enumerate(batch):
                items=sample["items"]
                values[index,:len(items)]=torch.tensor([scalar_value(item[source]) for item in items],dtype=dtype)
            result[target]=values

        return result
