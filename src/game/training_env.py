if __name__=="__main__":
    import sys
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/src")
    
   

#from room_server import RoomServer
import numpy as np
import asyncio
from game.train_agent import Agent_Train_Red as Agent_Train
from game.room import Room
from game.ppo_train import Agent_PPO
import torch
from torch import nn
from game.type_cards.creature import Creature
from game.type_cards.instant import Instant
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery


class Multi_Agent_Room(Room):
    """
    当回合开始的时候，向那个活跃的agent发送做动作的请求
    做好一个动作之后把状态奖励等放入agent里
    直到agent 做出了 0:end turn的这个动作
    """

    def __init__(self) -> None:
        self.agent1=Agent_PPO(271,352,name="agent1")
        self.agent2=Agent_PPO(271,352,name="agent2")
        # self.agent1.load_pth(
        #     "/Users/xuanpeichen/Desktop/code/python/openai/model_complete_act.pth",
        #     "/Users/xuanpeichen/Desktop/code/python/openai/model_complete_val.pth"
        # )
        # self.agent2.load_pth(
        #     "/Users/xuanpeichen/Desktop/code/python/openai/model_complete_act.pth",
        #     "/Users/xuanpeichen/Desktop/code/python/openai/model_complete_val.pth"
        # )

        super().__init__(None,None)


        self.action_process_condition=asyncio.Condition()#等待直到agent_cache不是空
        self.agent_cache=[]
         #store current player which is in his turn
        self.active_player:Agent_Train#进行操作的玩家
        self.non_active_player:Agent_Train

        

    def initinal_player(self,players:list[tuple]):
        agents_deck="Eternal Phoenix+Creature+4|Raging Firekin+Creature+4|Emberheart Salamander+Creature+4|Arcane Inferno+Instant+4|Pyroblast Surge+Instant+4|Fiery Blast+Instant+4|Inferno Titan+Creature+4|Flame Tinkerer+Creature+4|Mountain+Land+24"

        players=[(agents_deck,"Agent1"),(agents_deck,"Agent2")]
        
        self.player_1,self.player_2=Agent_Train(players[0][1],self,self.agent1),\
                                    Agent_Train(players[1][1],self,self.agent2)
        
        self.player_1.set_opponent_player(self.player_2,self)
        self.player_2.set_opponent_player(self.player_1,self)
        self.players:dict[Agent_Train]={
            players[0][1]:self.player_1,
            players[1][1]:self.player_2
        }

        self.players_socket:dict={
            players[0][1]:None,
            players[1][1]:None
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
    async def num2action(self,agent:Agent_Train,action:int)->str:
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

    def num2subaction(self,agent:Agent_Train,sub_action:int):
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


    async def process_action(self,agent:Agent_Train,action:int)->tuple:
        #将action 处理生成动作并且传入房间，将其挂起，直到房间处理好请求收到结束信号
        #如果是攻击的action，给敌方agent发送动作请求，自己挂起再一次，直到地方action动作做好发送信息给自己，自己结束挂起，计算state
        # 获取state，done，计算reward
        #返回new state 和 reward 和 done
        message:str=await self.num2action(agent,action)
        username,type,content=message.split("|")
        #old_reward=self.get_reward_red(agent)
        #print(username,content,type)
        await self.message_process_dict[type](username,content)

        if action>=2 and action <=11:
            agent_oppo:Agent_Train=agent.opponent
            state=self.get_state(agent_oppo)
            mask=self.create_action_mask(agent_oppo)
            action= agent_oppo.choose_action(*state,mask)
            #print(action)
            reward_func=await self.process_action(agent_oppo,action)
            asyncio.create_task(agent_oppo.store_data(state,action,reward_func))

        elif action!=0:
            await self.end_bullet_time()

        elif action==0:
            agent.notify_reward=False
        
        #change_reward=new_reward-old_reward

        async def next_state_function():
            new_reward=self.get_reward_red(agent)
            await self.check_death()
            die_player=await self.check_player_die()
            if die_player and agent.life<=0:
                new_reward=-1
            elif die_player:
                new_reward=1
            return self.get_state(agent),new_reward,self.gamming
        return next_state_function
        
    
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
    我方场地(10):[攻击力，生命值]/10 , [1,0]是否可以攻击和防御
    敌方场地(10):[攻击力，生命值]/10 , [1,0]是否可以攻击和防御
    时间状态[0,1]:本回合，敌方攻击
    攻击的随从[攻击力，生命值]/10
    """

    def get_state(self,agent:Agent_Train):
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


    def get_cost_total(self,agent:Agent_Train):
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
    def get_reward_red(self,agent:Agent_Train):#返回一个评分
        self_live_reward=lambda x :x/20#lambda x :1/(1+np.e**(4-x))#用于红色的公式，卖血
        oppo_live_reward=lambda x :x/20

        score_life_self=self_live_reward(agent.life)
        score_oppo_self=oppo_live_reward(agent.opponent.life)

        score_battle_self=sum([sum(card.state)/10 for card in agent.battlefield])#这个处以20表面随从不是很重要，重要的是敌方的血量
        score_battle_oppo=sum([sum(card.state)/10 for card in agent.battlefield])

        score_mana=0
        for land in agent.land_area:
            score_mana+=sum(land.generate_mana().values())
        score_mana=score_mana/20

        return (score_life_self-score_oppo_self)+score_mana+score_battle_self-score_battle_oppo






    #永远不会close game，只会initinal environment
    async def close_game(self,username:str,content:str):
        pass





    async def end_turn_time(self):#turn_timer is 0
        #self.non_active_player.
        self.action_processor.start_record()
        await self.change_turn()
        self.reset_turn_timer()
        self.action_processor.end_record()
        #触发一些回合开始的东西
        #开一个新的协程，从agent那里获取动作
        #asyncio.create_task(room.message_receiver("Agent2|...|..."))




    async def message_process(self):# 为了让每一个步骤变得有序
        while self.gamming:
            if not self.message_process_queue:
                async with self.message_process_condition:
                    await self.message_process_condition.wait_for(lambda: len(self.message_process_queue) > 0)  # 等待队列不为空
            func=self.message_process_queue.pop(0)
            await func[0](*func[1]) 
            await self.check_death()
            #这里做完之后继续向process action发送一个结束信号

    async def send_actioin_request(self,agent):#向agent发送需要动作的请求
        async with self.action_process_condition:
            self.agent_cache.append(agent)
            self.action_process_condition.notify() 

    async def action_process_system(self):#这个会等待，直到收到send_actioin_request发送的请求
        repeat_train=True
        while repeat_train:
            

            while self.gamming:
                agent:Agent_Train=self.active_player
                state=self.get_state(agent)
                mask=self.create_action_mask(agent)
                action=agent.choose_action(*state,mask)
                #print(action)
                reward_func=await self.process_action(agent,action)
                asyncio.create_task(agent.store_data(state,action,reward_func))
                await self.check_death()
                #print(self)
                
            #print("finish")
            self.gamming=True
            await self.initinal_environmrnt()
            
            
        #self.active_player.update()
        

    async def game_end(self,died_player:list[Agent_Train]):
        #self.gamming=False
        self.gamming=False

        for player in [self.player_1,self.player_2]:
            async with player.condition_reward:
                player.notify_reward=True
                player.condition_reward.notify()
        

    def create_action_mask(self,agent:Agent_Train):
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
                

    def mask_hand(self,agent:Agent_Train,oppo_agent:Agent_Train,mask:np.ndarray):
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






        





            

    



















from game.buffs import StateBuff
async def tasks(room):
    await asyncio.sleep(6)
    for name in room.players:
        room.players[name].draw_card(2)
        print("draw cards")
        print(room.action_store_list_cache)
    #asyncio.create_task(room.message_receiver("t|play_card|1"))
async def main():
    
    room=Multi_Agent_Room()
    
    await room.game_start()
    await room.action_process_system()
    #print([i.text(room.player_1) for i in room.player_1.hand])
    # room.active_player=room.players["Agent1"]
    # room.non_active_player=room.players["Agent2"]

    
    # print(room.get_reward_red(room.active_player))
    # mask=room.create_action_mask(room.active_player)
    # state=room.get_state(room.active_player)
    # print(mask)
    # action=room.active_player.choose_action(*state,mask)
    # print(action)

    # #act=(await room.num2action(room.active_player,action))
    # #print(act)

    # print(await room.process_action(room.active_player,action))
    
    # room.agent1.choose_act(*state)
    # room.agent1.store(state,10,1,state,0)
    # room.agent1.store(state,10,1,state,0)
    # room.agent1.train()
    
    # asyncio.create_task(room.message_receiver("Agent1|play_card|1"))
    # await asyncio.sleep(6)
    # print(room)
    # print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
    
    # asyncio.create_task(room.message_receiver("Agent1|play_card|1"))
    # await asyncio.sleep(6)
    # asyncio.create_task(room.message_receiver("Agent1|play_card|1"))
    
    # await asyncio.sleep(6)
    # asyncio.create_task(room.message_receiver("Agent1|activate_ability|land_area;0"))
    # await asyncio.sleep(1)
    # print(room)
    # print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
    
    # await asyncio.sleep(2)
    # asyncio.create_task(room.message_receiver("Agent1|play_card|0"))
    # await asyncio.sleep(6)
    # print(room)
    # print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
    
    # await asyncio.sleep(2)
    # asyncio.create_task(room.message_receiver("Agent1|end_step|"))
    # await asyncio.sleep(2)
    # asyncio.create_task(room.message_receiver("Agent2|play_card|1"))
    # await asyncio.sleep(6)
    # print(room)
    # print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
    
    
    # asyncio.create_task(room.message_receiver("Agent2|play_card|1"))
    # await asyncio.sleep(6)
    # asyncio.create_task(room.message_receiver("Agent2|play_card|1"))
    
    # await asyncio.sleep(6)
    # print(room)
    # print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
    
    # await asyncio.sleep(2)
    # asyncio.create_task(room.message_receiver("Agent2|play_card|0"))
    # await asyncio.sleep(6)
    # print(room)
    # print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
    
    # await asyncio.sleep(2)
    
    # await asyncio.sleep(5)
    # card=room.active_player.battlefield[0]
    # buff=StateBuff(card,2,2)
    # card.gain_buff(buff)
    # print(room)
    # print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
    
    # #card.loss_buff(buff)
    # #print(room)

    # await asyncio.sleep(2)
    # asyncio.create_task(room.message_receiver("Agent2|select_attacker|0"))
    
    # await asyncio.sleep(2)
    # print(room)
    # print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
    
    # asyncio.create_task(room.message_receiver("Agent1|select_defender|0"))
    # await asyncio.sleep(6)
    # print(room)
    # print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
        
if __name__=="__main__":
    
    
    asyncio.run(main())
    # print(np.zeros((3)))
    # a=np.zeros((10))

    # a[1:1]=True
    # print(a)
