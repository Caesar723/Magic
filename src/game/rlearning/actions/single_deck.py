from typing import TYPE_CHECKING
import numpy as np

from game.type_cards.creature import Creature
from game.type_cards.instant import Instant
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery

if TYPE_CHECKING:
    from game.agent import Agent_Player as Agent
    from game.base_agent_room import Base_Agent_Room
    




def create_sort_function(room:"Base_Agent_Room",agent:"Agent"):
    def sort_function(card:Creature):
        score=room.get_creature_reward(card)
        if agent.agent.config.get("sort_method","score")=="score_tap":
            if (not card.get_flag("summoning_sickness") or card.get_flag("haste")) and\
            not card.get_flag("tap") and (card.get_counter_from_dict("attack_counter")>0):
                score+=100
        return score
    return sort_function

def num2subaction(room:"Base_Agent_Room",agent:"Agent",sub_action:int):
    name=agent.name
    content=''
    father_class="field"
    type_act=""

    
    sort_function=create_sort_function(room,agent)
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



"""
0:end turn
1:end bullet time
2-11:选择一个随从进行攻击(10) 
12-21:选择一个随从进行阻挡(10)

22-1341
有10张手牌 对于每一张牌(40 * 33)
    player a card 不选择
    
    player a card 选择敌方随从0-9 总共10个随从
    player a card 选择我方随从0-9 总共10个随从

    player a card 选择敌方英雄
    player a card 选择我方英雄
    player a card 选择一个卡牌 (10)
"""
async def num2action(room:"Base_Agent_Room",agent:"Agent",action:int)->str:
    name=agent.name
    content=''
    sort_function=create_sort_function(room,agent)
    if action==0:
        type_act="end_step"
    elif action==1:
        type_act="end_bullet"
    elif action>=2 and action<=11:
        type_act="select_attacker"
        self_battlefield=agent.battlefield
        
        self_battlefield_sorted=sorted(enumerate(self_battlefield), key=lambda x: sort_function(x[1]), reverse=True)
        
        selected_index=self_battlefield_sorted[action-2][0]
        content=f'{selected_index}'
    elif action>=12 and action<=21:
        type_act="select_defender"
        
        self_battlefield=agent.battlefield
        
        self_battlefield_sorted=sorted(enumerate(self_battlefield), key=lambda x: sort_function(x[1]), reverse=True)
        
        selected_index=self_battlefield_sorted[action-12][0]
        content=f'{selected_index}'
    else:
        type_act="play_card"
        # print(action)
        # print(agent.id_dict)
        index_card=((action-22)//33)+1
        #print(index_card)
        key = next((k for k, v in agent.id_dict.items() if v == index_card), None)
        # print(key)
        # print(agent.hand)
        
        index_card=next((i for i, card in enumerate(agent.hand) if (f"{card.name}+{card.type}")==key), None)
        #print(index_card)
        content=f"{index_card}"
        sub_action=(action-22)%33
        sub_content=num2subaction(room,agent,sub_action)
        #print(sub_content)
        #print(sub_content)
        agent.set_select_content(sub_content)
        #print(sub_content)
    result=f"{name}|{type_act}|{content}"
    return result


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
        current_index=start_index+(agent.id_dict[f"{hand_card.name}+{hand_card.type}"]-1)*33
        if hand_card.check_can_use(agent)[0]:
            select_range=''
            for cls in instance_dict:
                if isinstance(hand_card,cls):
                    select_range=getattr(hand_card,instance_dict[cls]).select_range
            #print(select_range)
            if select_range in select_dict:
                select_stage(select_dict[select_range],index_range,current_index+1,mask)#+1 是因为有player a card 不选择
            elif hand_card.select_range in select_dict:
                select_stage(select_dict[hand_card.select_range],index_range,current_index+1,mask)
            else:
                mask[current_index]=True
        #start_index+=33
        card_counter+=1

def create_action_mask(room:"Base_Agent_Room",agent:"Agent"):
    oppo_agent=agent.opponent
    mask=np.zeros((1342))

    self_battlefield_sorted=sorted(agent.battlefield, key=create_sort_function(room,agent), reverse=True)
    if room.get_flag('attacker_defenders'):
        mask[1]=True
        for i,creat in enumerate(self_battlefield_sorted):
            if i>=10:break
                
            if not creat.get_flag("tap") and \
    (not room.attacker.get_flag("flying") or (creat.get_flag("flying") or creat.get_flag("reach"))):
                mask[12+i]=True
        #if agent.battlefield: mask[12:len(agent.battlefield)+12]=True
    else:
        mask[0]=True
        for i,creat in enumerate(self_battlefield_sorted):
            if i>=10:break
            if (not creat.get_flag("summoning_sickness") or creat.get_flag("haste")) and\
    not creat.get_flag("tap") and (creat.get_counter_from_dict("attack_counter")>0):
                mask[2+i]=True
        #if agent.battlefield: mask[2:len(agent.battlefield)+2]=True
        #print(agent.hand)
        if agent.hand:mask_hand(room,agent,oppo_agent,mask)
    
    return mask[np.newaxis, :]

