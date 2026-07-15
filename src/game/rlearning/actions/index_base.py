from typing import TYPE_CHECKING
import numpy as np

from game.type_cards.creature import Creature
from game.type_cards.instant import Instant,Instant_Undo
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery

if TYPE_CHECKING:
    from game.agent import Agent_Player as Agent
    from game.base_agent_room import Base_Agent_Room
    

"""
Gameplay action space (num2action / create_action_mask):
0: end turn
1: end bullet time
2-11: select a creature to attack with (10 choices)
12-21: select a creature to block with (10 choices)
22-31: activate an ability from a land-area slot (10 choices)
32-361: play card in hand slot * 33 sub-actions

Stack action encoding (action2num), 38 actions without index:
0: end_step
1: end_bullet
2: select_attacker
3: select_defender
4: activate_ability
5-37: play_card sub-action (33 variants)
"""
def select_stage(selects,index_range,start_index,mask):
    index=start_index
    for select_list,ind_range in zip(selects,index_range):
        length=min(len(select_list),10)
        mask[index:length+index]=True
        # for i in range(len(select_list)):
        #     mask[index+i]=True
        index+=ind_range



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


def mask_hand(room:"Base_Agent_Room",agent:"Agent",oppo_agent:"Agent",mask:np.ndarray):
    start_index=32

    select_dict={
        'all_roles':[oppo_agent.battlefield,agent.battlefield,[1],[1]],
        'opponent_roles':[oppo_agent.battlefield,[],[],[1]], 
        'your_roles':[[],agent.battlefield,[1],[]],
        'all_creatures':[oppo_agent.battlefield,agent.battlefield,[],[]],
        'opponent_creatures':[oppo_agent.battlefield,[],[],[]],
        'your_creatures':[[],agent.battlefield,[],[]],
        'all_lands':[oppo_agent.land_area,agent.land_area,[],[]],
        'opponent_lands':[oppo_agent.land_area,[],[],[]],
        'your_lands':[[],agent.land_area,[],[]]
    }

    index_range=[10,10,1,1]
    #getattr(obj, 'my_attribute')
    card_counter=0
    for hand_card in agent.hand:
        if room.get_flag("bullet_time"):
            if not isinstance(hand_card,Instant) and not hand_card.get_flag("Flash"):
                start_index+=33
                card_counter+=1
                continue
        
        if card_counter>=10:
            break
        if hand_card.check_can_use(agent)[0]:
            select_range=get_card_select_range(hand_card)
            #print(select_range)
            if select_range in select_dict:
                select_stage(select_dict[select_range],index_range,start_index+1,mask)#+1 是因为有player a card 不选择
            elif hand_card.select_range in select_dict:
                select_stage(select_dict[hand_card.select_range],index_range,start_index+1,mask)
            else:
                mask[start_index]=True
        start_index+=33
        card_counter+=1


def mask_land_abilities(agent:"Agent",oppo_agent:"Agent",mask:np.ndarray):
    """Expose usable land abilities in every priority window."""
    for index, land in enumerate(agent.land_area[:10]):
        if not land.get_flag("tap") and land.check_ability_can_be_used(agent, oppo_agent):
            mask[22+index]=True


def create_action_mask(room:"Base_Agent_Room",agent:"Agent"):
    oppo_agent=agent.opponent
    mask=np.zeros((362))
    mask_land_abilities(agent,oppo_agent,mask)
    if room.get_flag('attacker_defenders'):
        mask[1]=True
        for i,creat in enumerate(agent.battlefield):
            if i>=10:break
            if not creat.get_flag("tap") and \
    (not room.attacker.get_flag("flying") or (creat.get_flag("flying") or creat.get_flag("reach"))):
                mask[12+i]=True
        #if agent.battlefield: mask[12:len(agent.battlefield)+12]=True
        if agent.hand:
            mask_hand(room,agent,oppo_agent,mask)
    elif room.get_flag("bullet_time"):
        if agent.hand:
            mask_hand(room,agent,oppo_agent,mask)
    else:
        mask[0]=True
        for i,creat in enumerate(agent.battlefield):
            if i>=10:break
            if (not creat.get_flag("summoning_sickness") or creat.get_flag("haste")) and\
    not creat.get_flag("tap") and (creat.get_counter_from_dict("attack_counter")>0):
                mask[2+i]=True
        #if agent.battlefield: mask[2:len(agent.battlefield)+2]=True
        if agent.hand:mask_hand(room,agent,oppo_agent,mask)
    #print(mask)
    return mask[np.newaxis, :]

def num2subaction(room:"Base_Agent_Room",agent:"Agent",sub_action:int,select_range:str=""):
    name=agent.name
    content=''
    father_class="field"
    type_act=""

    
    sort_function=room.create_sort_function(agent)
    if sub_action==0:
        pass
    elif sub_action>=1 and sub_action<=10:
        if select_range in ("all_lands","opponent_lands"):
            type_act="opponent_landfield"
            selected_index=sub_action-1
        else:
            opponent_battlefield=agent.opponent.battlefield
            opponent_battlefield_sorted=sorted(enumerate(opponent_battlefield), key=lambda x: sort_function(x[1]), reverse=True)
            type_act="opponent_battlefield"
            selected_index=opponent_battlefield_sorted[sub_action-1][0]
        content=f"{selected_index}"
    elif sub_action>=11 and sub_action<=20:
        if select_range in ("all_lands","your_lands"):
            type_act="self_landfield"
            selected_index=sub_action-11
        else:
            self_battlefield=agent.battlefield
            self_battlefield_sorted=sorted(enumerate(self_battlefield), key=lambda x: sort_function(x[1]), reverse=True)
            selected_index=self_battlefield_sorted[sub_action-11][0]
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
    sort_function=room.create_sort_function(agent)
    if father_class=="field":
        if not type_act:
            return 0
        if type_act=="opponent_battlefield":
            opponent_battlefield_sorted=sorted(enumerate(agent.opponent.battlefield), key=lambda x: sort_function(x[1]), reverse=True)
            selected_index=int(content)
            for rank,(idx,_) in enumerate(opponent_battlefield_sorted):
                if idx==selected_index:
                    return rank+1
            raise ValueError(f"opponent battlefield index {selected_index} not found")
        if type_act=="self_battlefield":
            self_battlefield_sorted=sorted(enumerate(agent.battlefield), key=lambda x: sort_function(x[1]), reverse=True)
            selected_index=int(content)
            for rank,(idx,_) in enumerate(self_battlefield_sorted):
                if idx==selected_index:
                    return rank+11
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


def add_action_history(agent:"Agent",batch):
    pass