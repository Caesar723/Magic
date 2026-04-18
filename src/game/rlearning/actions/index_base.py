from typing import TYPE_CHECKING
import numpy as np

from game.type_cards.creature import Creature
from game.type_cards.instant import Instant
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery

if TYPE_CHECKING:
    from game.agent import Agent_Player as Agent
    from game.base_agent_room import Base_Agent_Room
    


def select_stage(selects,index_range,start_index,mask):
    index=start_index
    for select_list,ind_range in zip(selects,index_range):
        length=min(len(select_list),10)
        mask[index:length+index]=True
        # for i in range(len(select_list)):
        #     mask[index+i]=True
        index+=ind_range



def mask_hand(room:"Base_Agent_Room",agent:"Agent",oppo_agent:"Agent",mask:np.ndarray):
    start_index=22
    instance_dict={
        Creature:"when_enter_battlefield",
        Instant:"card_ability",
        Land:"when_enter_landarea",
        Sorcery:"card_ability"
    }

    select_dict={
        'all_roles':[oppo_agent.battlefield,agent.battlefield,[1],[1]],
        'opponent_roles':[oppo_agent.battlefield,[],[],[1]], 
        'your_roles':[[],agent.battlefield,[1],[]],
        'all_creatures':[oppo_agent.battlefield,agent.battlefield,[],[]],
        'opponent_creatures':[oppo_agent.battlefield,[],[],[]],
        'your_creatures':[[],agent.battlefield,[],[]]
    }

    index_range=[10,10,1,1]
    #getattr(obj, 'my_attribute')
    card_counter=0
    for hand_card in agent.hand:
        if card_counter>=9:
            break
        if hand_card.check_can_use(agent)[0]:
            select_range=''
            for cls in instance_dict:
                if isinstance(hand_card,cls):
                    select_range=getattr(hand_card,instance_dict[cls]).select_range
            #print(select_range)
            if select_range in select_dict:
                select_stage(select_dict[select_range],index_range,start_index+1,mask)#+1 是因为有player a card 不选择
            elif hand_card.select_range in select_dict:
                select_stage(select_dict[hand_card.select_range],index_range,start_index+1,mask)
            else:
                mask[start_index]=True
        start_index+=33
        card_counter+=1


def create_action_mask(room:"Base_Agent_Room",agent:"Agent"):
    oppo_agent=agent.opponent
    mask=np.zeros((352))
    if room.get_flag('attacker_defenders'):
        mask[1]=True
        for i,creat in enumerate(agent.battlefield):
            if i>=10:break
            if not creat.get_flag("tap") and \
    (not room.attacker.get_flag("flying") or (creat.get_flag("flying") or creat.get_flag("reach"))):
                mask[12+i]=True
        #if agent.battlefield: mask[12:len(agent.battlefield)+12]=True
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

def num2subaction(room:"Base_Agent_Room",agent:"Agent",sub_action:int):
    name=agent.name
    content=''
    father_class="field"
    type_act=""

    
    sort_function=room.create_sort_function(agent)
    if sub_action==0:
        pass
    elif sub_action>=1 and sub_action<=10:
        opponent_battlefield=agent.opponent.battlefield
        opponent_battlefield_sorted=sorted(enumerate(opponent_battlefield), key=lambda x: sort_function(x[1]), reverse=True)
        type_act="opponent_battlefield"
        selected_index=opponent_battlefield_sorted[sub_action-1][0]
        content=f"{selected_index}"
    elif sub_action>=11 and sub_action<=20:
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
    else:
        type_act="play_card"
        index_card=(action-22)//33
        content=f"{index_card}"
        sub_action=(action-22)%33
        sub_content=num2subaction(room,agent,sub_action)
        agent.set_select_content(sub_content)
        #print(sub_content)
    result=f"{name}|{type_act}|{content}"
    return result