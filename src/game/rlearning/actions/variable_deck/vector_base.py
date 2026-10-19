from typing import TYPE_CHECKING
import numpy as np
import torch
from game.type_cards.creature import Creature
from game.type_cards.instant import Instant,Instant_Undo
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery
from game.rlearning.states.variable_deck.full_state import get_state_from_player,index_to_action,get_current_state
if TYPE_CHECKING:
    from game.agent import Agent_Player as Agent
    from game.base_agent_room import Base_Agent_Room
    





def create_action_mask(room:"Base_Agent_Room",agent:"Agent"):
    return None


def append_history(state:dict,history:list,history_length:int=10):
    if 0 in history:
        history.clear()
    if history_length <= 0:
        history.clear()
        return
    history.append(state)
    if len(history)>history_length:
        history.pop(0)

def first_numpy(value):
    if torch.is_tensor(value):
        value = value.detach().cpu().numpy()
    return np.asarray(value[0]).copy()


def first_int(value):
    if torch.is_tensor(value):
        value = value.detach().cpu().numpy()
    return int(np.asarray(value).reshape(-1)[0])

def add_history(agent:"Agent",batch):
    required = ("selected_planner", "selected_mean", "selected_std")
    missing = [key for key in required if key not in batch]
    if missing:
        raise KeyError(f"add_history missing model outputs: {missing}")
    action = first_int(batch["action"])
    record = {
        "state": get_current_state(agent.room, agent),
        "action": action,
        "sampled_log_prob": first_numpy(batch["sampled_log_prob"]),
        "value": first_numpy(batch["value"]),
        "candidate_slot": first_int(batch["candidate_slot"]),
        "planner": first_numpy(batch["selected_planner"]),
        "mean_p": first_numpy(batch["selected_mean"]),
        "std_p": first_numpy(batch["selected_std"]),
    }

    max_seq_len = agent.config.get("max_seq_len", agent.action_history_length)
    append_history(record, agent.action_history, max_seq_len)
    return record


def add_opponent_history(agent:"Agent",opponent_agent:"Agent",message:str):
    index=action2num(agent.room,opponent_agent,message)
    info={
        "state":get_state_from_player(agent.room,opponent_agent),
        "message":message,
        "index":index,
        "action":index_to_action(index)
    }
    append_history(info,agent.opponent_history,agent.opponent_history_length)
    return info


def num2subaction(room:"Base_Agent_Room",agent:"Agent",sub_action:int,select_range:str=""):
    name=agent.name
    content=''
    father_class="field"
    type_act=""

    
    if sub_action==0:
        pass
    elif sub_action>=1 and sub_action<=10:
        if select_range in ("all_lands","opponent_lands"):
            type_act="opponent_landfield"
            selected_index=sub_action-1
        else:
            type_act="opponent_battlefield"
            selected_index=sub_action-1
        content=f"{selected_index}"
    elif sub_action>=11 and sub_action<=20:
        if select_range in ("all_lands","your_lands"):
            type_act="self_landfield"
            selected_index=sub_action-11
        else:
            selected_index=sub_action-11
            type_act="self_battlefield"
        content=f"{selected_index}"
    elif sub_action==21:
        type_act="oppo"
    elif sub_action==22:
        type_act="self"
    else:
        father_class="cards"
        type_act=f"{sub_action-11}"
        content=""
    result=f"{name}|{father_class}|{type_act}|{content}"
    return result


def subaction2num(room:"Base_Agent_Room",agent:"Agent",sub_content:str)->int:
    if not sub_content:
        return 0
    _,father_class,type_act,content,*_=sub_content.split("|")
    if father_class=="field":
        if not type_act:
            return 0
        if type_act=="opponent_battlefield":
            selected_index=int(content)
            if 0<=selected_index<min(len(agent.opponent.battlefield),10):
                return selected_index+1
            raise ValueError(f"opponent battlefield index {selected_index} not found")
        if type_act=="self_battlefield":
            selected_index=int(content)
            if 0<=selected_index<min(len(agent.battlefield),10):
                return selected_index+11
            raise ValueError(f"self battlefield index {selected_index} not found")
        if type_act=="opponent_landfield":
            selected_index=int(content)
            if 0<=selected_index<min(len(agent.opponent.land_area),10):
                return selected_index+1
            raise ValueError(f"opponent land index {selected_index} not found")
        if type_act=="self_landfield":
            selected_index=int(content)
            if 0<=selected_index<min(len(agent.land_area),10):
                return selected_index+11
            raise ValueError(f"self land index {selected_index} not found")
        if type_act=="oppo":
            return 21
        if type_act=="self":
            return 22
    elif father_class=="cards":
        return int(type_act)+11
    raise ValueError(f"unknown sub action content: {sub_content}")


def _split_action_message(message:str)->tuple[str,str]:
    if "||" in message:
        message,select_content=message.split("||",1)
        return message,select_content
    return message,None



def action2num(room:"Base_Agent_Room",agent:"Agent",message:str,select_content:str=None)->int:
    message,merged_select_content=_split_action_message(message)
    if select_content is None:
        select_content=merged_select_content
    _,type_act,_=message.split("|")
    if type_act=="end_step":
        return 0
    if type_act=="end_bullet":
        return 1
    if type_act=="select_attacker":
        return 2
    if type_act=="select_defender":
        return 3
    if type_act=="activate_ability":
        return 4
    if type_act=="play_card":
        if select_content is None:
            select_content = agent.select_content
        sub_action = subaction2num(room, agent, select_content)
        return 5 + sub_action
    raise ValueError(f"unknown action message: {message}")


def get_card_select_range(card):
    instance_dict={
        Creature:"when_enter_battlefield",
        Instant:"card_ability",
        Land:"when_enter_landarea",
        Sorcery:"card_ability"
    }
    for cls, ability_name in instance_dict.items():
        if isinstance(card,cls):
            return getattr(card,ability_name).select_range
    return ""


async def num2action(room:"Base_Agent_Room",agent:"Agent",action:int)->str:
    name=agent.name
    content=''
    if action==0:
        type_act="end_step"
    elif action==1:
        type_act="end_bullet"
    elif action>=2 and action<=11:
        type_act="select_attacker"
        content=f'{action-2}'
    elif action>=12 and action<=21:
        type_act="select_defender"
        content=f'{action-12}'
    elif action>=22 and action<=31:
        type_act="activate_ability"
        content=f'land_area;{action-22}'
    else:
        type_act="play_card"
        index_card=(action-32)//33
        content=f"{index_card}"
        sub_action=(action-32)%33
        select_range=get_card_select_range(agent.hand[index_card])
        sub_content=num2subaction(room,agent,sub_action,select_range)
        agent.set_select_content(sub_content)
        #print(sub_content)
    result=f"{name}|{type_act}|{content}"
    return result
