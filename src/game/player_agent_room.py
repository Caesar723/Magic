if __name__=="__main__":
    import sys
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/src")
    
   

#from room_server import RoomServer
import numpy as np
import asyncio
#from game.train_agent import Agent_Train_Red as Agent_Train
from game.room import Room
from game.ppo_train import Agent_PPO
from game.player import Player
from game.agent import Agent_Player_Red as Agent
import torch
from torch import nn
from game.type_cards.creature import Creature
from game.type_cards.instant import Instant
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery


class PVE_Room(Room):
    """
    当回合开始的时候，向那个活跃的agent发送做动作的请求
    做好一个动作之后把状态奖励等放入agent里
    直到agent 做出了 0:end turn的这个动作
    """

    def __init__(self,players:list[tuple],room_server) -> None:
        #self.agent1=Agent_PPO(251,352)
        
        super().__init__(players,room_server)


        self.action_process_condition=asyncio.Condition()#等待直到agent_cache不是空
        self.agent_cache=[]
         #store current player which is in his turn
        self.active_player:"Agent|Player"#进行操作的玩家
        self.non_active_player:"Agent|Player"

        

    def initinal_player(self,players:list[tuple]):
        #agents_deck="Eternal Phoenix+Creature+4|Raging Firekin+Creature+4|Emberheart Salamander+Creature+4|Arcane Inferno+Instant+4|Pyroblast Surge+Instant+4|Fiery Blast+Instant+4|Inferno Titan+Creature+4|Flame Tinkerer+Creature+4|Mountain+Land+24"

        # Agent_para=[(agents_deck,"Agent1")]
        
        self.player_1,self.player_2=Agent("Agent1",self.action_processor),\
                                    Player(players[0][1],players[0][0],self.action_processor)
        self.player_1.set_opponent_player(self.player_2,self)
        self.player_2.set_opponent_player(self.player_1,self)
        self.players:dict={
            "Agent1":self.player_1,
            players[0][1]:self.player_2
        }

        self.players_socket:dict={
            "Agent1":None,
            players[0][1]:None
        }

    async def initinal_environmrnt(self):# 返回一个state和评分
        self.initinal_player(None)
        await self.game_start()


    """
    0:end turn
    1:end bullet time
    2-11:选择一个随从进行攻击(10) 
    12-21:选择一个随从进行阻挡(10)

    22-351
    有10张手牌 对于每一张牌(10 * 33)
        player a card 不选择
        
        player a card 选择敌方随从0-9 总共10个随从
        player a card 选择我方随从0-9 总共10个随从

        player a card 选择敌方英雄
        player a card 选择我方英雄
        player a card 选择一个卡牌 (10)
    """
    async def num2action(self,agent:Agent,action:int)->str:
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
            sub_content=self.num2subaction(agent,sub_action)
            agent.set_select_content(sub_content)
            #print(sub_content)
        result=f"{name}|{type_act}|{content}"
        return result

    def num2subaction(self,agent:Agent,sub_action:int):
        name=agent.name
        content=''
        father_class="field"
        type_act=""

        if sub_action==0:
            pass
        elif sub_action>=1 and sub_action<=10:
            type_act="opponent_battlefield"
            content=f"{sub_action-1}"
        elif sub_action>=11 and sub_action<=20:
            type_act="self_battlefield"
            content=f"{sub_action-11}"
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


    async def process_action(self,agent:Agent,action:int)->tuple:
        #将action 处理生成动作并且传入房间，将其挂起，直到房间处理好请求收到结束信号
        #如果是攻击的action，给敌方agent发送动作请求，自己挂起再一次，直到地方action动作做好发送信息给自己，自己结束挂起，计算state
        # 获取state，done，计算reward
        #返回new state 和 reward 和 done
        message:str=await self.num2action(agent,action)
        print(message)
        await self.message_receiver(message)
        # username,type,content=message.split("|")
        # await self.message_process_dict[type](username,content)
        
        return 
    
    def get_flag(self,flag_name:str):
        key="{}_bullet_time_flag"
        if flag_name==key.format("Agent1"):
            return True
        if flag_name in self.flag_dict:
            
            return self.flag_dict[flag_name]
        else:
            return False
    
    async def check_player_die(self):
        died_player=[]
        for name in self.players:
            if (await self.players[name].check_dead()):
                died_player.append(self.players[name])
        return bool(died_player)




    """
    让状态归一
    1-我方英雄的血量/20
    1-敌方英雄的血量/20
    蓝色，红色，绿色，白色，黑色法力值（通过计算地牌来得出）/10
    卡牌(10):[编号，法力值]使用嵌入式（10*20）
        # 定义嵌入层
        # card_embedding = tf.keras.layers.Embedding(input_dim=100, output_dim=14)  # 卡牌编号的嵌入层
        (0,0,0,0,0,0)
        # hand_cards_embedded = tf.concat([
        #     card_embedding(hand_cards[:, 0]),
        #     mana_embedding(hand_cards[:, 1])
        # ], axis=-1)
    我方场地(10):[攻击力，生命值]/10
    敌方场地(10):[攻击力，生命值]/10
    时间状态[0,1]:本回合，敌方攻击
    攻击的随从[攻击力，生命值]/10
    """

    def get_state(self,agent:Agent):
        oppo_agent=agent.opponent

        self_life=1-agent.life/agent.ini_life
        oppo_life=1-oppo_agent.life/oppo_agent.ini_life

        lifes=np.array([self_life,oppo_life])

        cost=self.get_cost_total(agent)
        colors=np.array([cost["U"],cost["R"],cost["G"],cost["W"],cost["B"]])

        cards_hand_costs=[]
        length_hand=len(agent.hand)
        for hand_i in range(10):
            if hand_i <length_hand:
                card=agent.hand[hand_i]
                cards_hand_costs.append(list(card.calculate_cost().values()))
            else:
                cards_hand_costs.append([0,0,0,0,0,0])
        cards_hand_costs=np.array(cards_hand_costs)
        cards_hand_costs=cards_hand_costs.flatten()/10

        self_battlefield=self.get_creature_state(agent.battlefield)
        oppo_battlefield=self.get_creature_state(oppo_agent.battlefield)

        time_state=self.get_time_state()

        attacker=self.get_attacker()

        cards_id=[]
        for id_i in range(10):
            if id_i <length_hand:
                card=agent.hand[id_i]
                cards_id.append(agent.id_dict[f"{card.name}+{card.type}"])
            else:
                cards_id.append(0)

        cards_id=np.array(cards_id)
        
        num_state=np.concatenate((lifes,colors,cards_hand_costs,self_battlefield,oppo_battlefield,time_state,attacker))

        return num_state,cards_id



    def get_creature_state(self,array:list[Creature]):
        length=len(array)
        result=[]
        for i in range(10):
            if i < length:
                activate=[0]
                if not array[i].get_flag("tap") and not array[i].get_flag("summoning_sickness"):
                    activate=[10]
                result.append(list(array[i].state)+activate)
            else:
                result.append([0,0,0])
        result=np.array(result)
        result=result.flatten()/10
        return result
    
    def get_time_state(self):
        return np.array([0,1] if self.get_flag("attacker_defenders") else [1,0])
    
    def get_attacker(self):
        if self.get_flag("attacker_defenders"):
            result=list(self.attacker.state)
        else:
            result=[0,0]
        result=np.array(result)/10
        return result


    def get_cost_total(self,agent:Agent):
        player_mana=dict(agent.mana)
        for land in agent.land_area:
            if not land.get_flag("tap"):
                mana=land.generate_mana()
                for key in mana:
                    player_mana[key]+=mana[key]
        return player_mana


        

    #将 (英雄的血量/20)+(（随从的血量/攻击力）/20)   -((英雄的血量/20)+(（随从的血量/攻击力）/20)) 因为是红色的注重与敌方的血量
    # 
    #还有法力值上限也需要考虑
    #reward 是上面奖励的变化量
    def get_reward_red(self,agent:Agent):#返回一个评分
        self_live_reward=lambda x :1/(1+np.e**(4-x))#用于红色的公式，卖血
        oppo_live_reward=lambda x :x/20

        score_life_self=self_live_reward(agent.life)
        score_oppo_self=oppo_live_reward(agent.opponent.life)

        score_battle_self=sum([sum(card.state)/20 for card in agent.battlefield])#这个处以20表面随从不是很重要，重要的是敌方的血量
        score_battle_oppo=sum([sum(card.state)/20 for card in agent.battlefield])

        score_mana=0
        for land in agent.land_area:
            score_mana+=sum(land.generate_mana().values())
        score_mana=score_mana/20

        return (score_life_self-score_oppo_self)+score_mana+score_battle_self-score_battle_oppo






    def create_action_mask(self,agent:Agent):
        oppo_agent=agent.opponent
        mask=np.zeros((352))
        if self.get_flag('attacker_defenders'):
            mask[1]=True
            for i,creat in enumerate(agent.battlefield):
                if not creat.get_flag("tap") and not creat.get_flag("summoning_sickness"):
                    mask[12+i]=True
            #if agent.battlefield: mask[12:len(agent.battlefield)+12]=True
        else:
            mask[0]=True
            for i,creat in enumerate(agent.battlefield):
                if not creat.get_flag("tap") and not creat.get_flag("summoning_sickness"):
                    mask[2+i]=True
            #if agent.battlefield: mask[2:len(agent.battlefield)+2]=True
            if agent.hand:self.mask_hand(agent,oppo_agent,mask)
        
        return mask[np.newaxis, :]
                

    def mask_hand(self,agent:Agent,oppo_agent:Agent,mask:np.ndarray):
        start_index=22
        instance_dict={
            Creature:"when_enter_battlefield",
            Instant:"card_ability",
            Land:"when_enter_battlefield",
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
                    self.select_stage(select_dict[select_range],index_range,start_index+1,mask)#+1 是因为有player a card 不选择
                elif hand_card.select_range in select_dict:
                    self.select_stage(select_dict[hand_card.select_range],index_range,start_index+1,mask)
                else:
                    mask[start_index]=True
            start_index+=33
            card_counter+=1


    def select_stage(self,selects,index_range,start_index,mask):
        index=start_index
        for select_list,ind_range in zip(selects,index_range):
            length=min(len(select_list),10)
            mask[index:length+index]=True
            # for i in range(len(select_list)):
            #     mask[index+i]=True
            index+=ind_range

    async def ask_agent_do_act(self):
        await asyncio.sleep(1)
        agent:Agent=self.player_1
        state=self.get_state(agent)
        mask=self.create_action_mask(agent)
        action=agent.choose_action(*state,mask)
        print(action)
        return await self.process_action(agent,action)


    async def end_bullet_time(self):
        result= await super().end_bullet_time() 
        if self.active_player.name=="Agent1":
            await self.ask_agent_do_act()
        return result
    
    async def select_attacker(self, username: str, content: str):
        result=await super().select_attacker(username, content)
        if username!="Agent1" and result[0]:
            print(await self.ask_agent_do_act())
        return result
    
    async def end_turn_time(self):
        await super().end_turn_time()
        if self.active_player.name=="Agent1":
            await self.ask_agent_do_act()

    async def game_start(self):
        await super().game_start()
        if self.active_player.name=="Agent1":
            await self.ask_agent_do_act()
         






        





            

    















