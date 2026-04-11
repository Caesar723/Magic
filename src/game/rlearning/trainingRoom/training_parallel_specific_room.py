import sys
if __name__=="__main__":
    
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/src")
    
   
import inspect
import traceback
#from room_server import RoomServer
import numpy as np
import asyncio
import random
import os
import time
from multiprocessing import Process, Queue

from game.train_agent import Agent_Train 
from game.room import Room
from game.ppo_train import Agent_PPO
from game.rlearning.module.ppo_agent import PPOTrainer
from game.rlearning.utils.model import get_class_by_name
from initinal_file import CARD_DICTION
from game.card import Card
from game.type_cards.creature import Creature
from game.type_cards.instant import Instant
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery
from game.testing_room import Testing_Spawn_Creature
from game.player import Player
from game.rlearning.trainingRoom.training_parallel_room import Multi_Agent_Parallel_Room
from typing import TYPE_CHECKING
from game.game_function_tool import get_dir_names,name_replace,ORGPATH
import re
if TYPE_CHECKING:
    from game.rlearning.communicate.training_parallel_specific_room import Info_Communication




class Multi_Agent_Parallel_Specific_Room(Multi_Agent_Parallel_Room):

    CARDS_CACHE:dict[str,list[Card]]={}

    def __init__(self, env_config, info_communication:"Info_Communication", worker_id:int):
        self.env_config=env_config
        super().__init__(env_config, info_communication, worker_id)
        
        
        Agent_Train.send_selection_cards.__defaults__=(True,True)
        Agent_Train.send_selection_cards.__defaults__=(True,True)

    def change_environmrnt(self):
        self.action_store_list_cache=[]

        simulate=[
            (self.simulate_play,"play"),
            (self.simulate_creature_attack,"attack"),
            (self.simulate_creature_defend,"defend"),
        ]
        
        graveyard=[
            self.env_initinal_graveyard
        ]
        hand=[
            self.env_initinal_hand
        ]
        library=[
            self.env_initinal_library
        ]
        battlefield_self=[
            (self.env_creature,["play","attack","defend"]),
            (self.env_no_creature,["play","attack","defend"]),
            (self.env_one_creature,["play","attack","defend"]),
        ]
        battlefield_oppo=[
            (self.env_creature,["play","attack","defend"]),
            (self.env_no_creature,["play","attack"]),
            (self.env_one_creature,["play","attack","defend"]),
        ]
        life_self=[
            (self.env_life_low,["play","attack","defend"]),
            (self.env_life_middle,["play","attack","defend"]),
            (self.env_life_high,["play","attack","defend"]),
        ]
        life_oppo=[
            (self.env_life_low,["play","attack","defend"]),
            (self.env_life_middle,["play","attack","defend"]),
            (self.env_life_high,["play","attack","defend"]),
        ]
        mana=[
            self.env_high_mana,
        ]
        self.clear_environmrnt()

        simulate_func,simulate_type=random.choice(simulate)

        random.choice(graveyard)(self.player_1)
        random.choice(hand)(self.player_1)
        random.choice(library)(self.player_1)
        self.get_filtered_func(battlefield_self,simulate_type)(self.player_1)
        self.get_filtered_func(battlefield_oppo,simulate_type)(self.player_2)
        self.get_filtered_func(life_self,simulate_type)(self.player_1)
        self.get_filtered_func(life_oppo,simulate_type)(self.player_2)
        random.choice(mana)(self.player_1)

        simulate_info=simulate_func()
        


        for recorder_key in self.game_recorder:
            recorder=self.game_recorder[recorder_key]
            recorder.store_game_message(self.text(self.players[recorder_key]))

        return simulate_info

    def get_filtered_func(self,func_list:list[tuple],simulate_type:str):
        result=[]
        for func,types in func_list:
            if simulate_type in types:
                result.append(func)
        result=random.choice(result)
        return result

    def clear_environmrnt(self):
        self.flag_dict:dict={}
        self.counter_dict:dict={}
        self.attacker:Creature=None
        self.clear_player_environmrnt(self.player_1)
        self.clear_player_environmrnt(self.player_2)

    def clear_player_environmrnt(self,player):
        player.graveyard=[]
        player.hand=[]
        player.library=[]
        player.battlefield=[]
        player.life=[]
        player.land_area=[]
        player.exile_area=[]
        player.treasure=[]
        player.counter_dict={}
        player.counter_dict["lands_summon_max"]=1
        player.flag_dict={}
        player.mana={"colorless":0,"U":0,"W":0,"B":0,"R":0,"G":0}
        player.cards_store_dict:dict[list]={}
        player.aura_pool:list[Card]=[]


    def get_cards_sample_by_name(self,name:str,number:int,is_except=False):
        if name == "undo":
            print("get_cards_sample_by_name",name,number,is_except)
            result=[]
            types=["Instant"]
            subclass_dict={"Instant_Undo":"Instant"}
            class_dict={}
            for type in types:
                directory_path=f"{ORGPATH}/cards/{type}"
                for name in get_dir_names(directory_path):
                    class_name=name_replace(name)
                    class_dict[class_name]=name
            for subclass in Card.__subclasses__():
                for card in subclass.__subclasses__():
                    try:
                        class_name = re.sub(r'__$', '', card.__name__)
                        if class_name in subclass_dict:
                            if not is_except:
                                for subcard in card.__subclasses__():
                                    result.append(f"{class_dict[subcard.__name__]}_{subclass_dict[class_name]}")
                        else:
                            if is_except:
                                result.append(f"{class_dict[class_name]}_{subclass.__name__}")
                    except KeyError as e:
                        pass
            
        else:
            #print("get_cards_sample_by_name",name,number,is_except)
            if is_except:
                result=[
                    key for key in CARD_DICTION if name not in key.lower()
                ]
            else:
                result=[
                    key for key in CARD_DICTION if name in key.lower()
                ]
            
        # if name in self.CARDS_CACHE:
        #     return self.CARDS_CACHE[name]
        # else:
        #     self.CARDS_CACHE[name]=result
        result=random.sample(result,number)
        return result


    def env_initinal_library(self,player):
        cards=["Plains_Land","Island_Land","Swamp_Land","Mountain_Land","Forest_Land"]
        creature_cards=self.get_cards_sample_by_name("creature",2)
        instant_cards=self.get_cards_sample_by_name("instant",2)
        sorcery_cards=self.get_cards_sample_by_name("sorcery",2)
        land_cards=self.get_cards_sample_by_name("land",2)
        player.library=[
            CARD_DICTION[key](player)
            for key in creature_cards+instant_cards+sorcery_cards+land_cards+cards
        ]
        random.shuffle(player.library)

    
    def env_initinal_graveyard(self,player):
        cards=["Plains_Land","Island_Land","Swamp_Land","Mountain_Land","Forest_Land"]
        creature_cards=self.get_cards_sample_by_name("creature",2)
        instant_cards=self.get_cards_sample_by_name("instant",2)
        sorcery_cards=self.get_cards_sample_by_name("sorcery",2)
        land_cards=self.get_cards_sample_by_name("land",2)
        player.graveyard=[
            CARD_DICTION[key](player)
            for key in creature_cards+instant_cards+sorcery_cards+land_cards+cards
        ]
        random.shuffle(player.graveyard)

    def env_initinal_hand(self,player):
        return 
        

    def env_life_low(self,player):
        life=random.randint(1,7)
        player.life=life
        player.ini_life=life
    def env_life_middle(self,player):
        life=random.randint(8,14)
        player.life=life
        player.ini_life=life
    def env_life_high(self,player):
        life=random.randint(15,20)
        player.life=life
        player.ini_life=life

    def get_creature_sample(self, weight: float):
        """
        根据0~1的float权重生成一个随从样本，使用随机分配的方式，从总点数中抽取攻击和生命。
        flag数量略少且受权重影响较弱。
        """
        weight = max(0.0, min(weight, 1.0))
        flag_pool = [
            "flying", "trample", "haste", "first strike", "lifelink", "vigilance", "deathtouch", "hexproof", "reach"
        ]

        min_total_stat = 2     # 最低攻击+生命之和
        max_total_stat = 12    # 最高攻击+生命之和
        min_flags = 0
        max_flags = 1          # flag数量整体下调，最高只给1个

        # 总强度分配
        total_stat = int(round(min_total_stat + (max_total_stat - min_total_stat) * weight))
        flag_count = int(round(min_flags + (max_flags - min_flags) * weight))
        flag_count = max(0, min(flag_count, max_flags))

        # 至少分1点到攻击和生命
        remain_points = total_stat - 2
        points = [1, 1]  # 先给power和toughness各分1点
        # 剩余点数随机分配到power和toughness
        for _ in range(remain_points):
            idx = random.randint(0, 1)
            points[idx] += 1
        power, toughness = points

        chosen_flags = {}
        if flag_count > 0:
            sampled_flags = random.sample(flag_pool, flag_count)
            for key in sampled_flags:
                chosen_flags[key] = True

        return {
            "power": power,
            "toughness": toughness,
            "flag_keywords": chosen_flags
        }


    
    def env_one_creature(self,player:"Player"):
        weight=random.random()
        creature_sample=self.get_creature_sample(weight)
        creature=Testing_Spawn_Creature(player,creature_sample["power"],creature_sample["toughness"],creature_sample["flag_keywords"])
        player.battlefield=[creature]

    def env_no_creature(self,player):
        player.battlefield=[]
    def env_creature(self,player:"Player"):
        num=random.randint(1,6)
        creatures=[]
        for i in range(num):
            weight=random.random()
            creature_sample=self.get_creature_sample(weight)
            creature=Testing_Spawn_Creature(player,creature_sample["power"],creature_sample["toughness"],creature_sample["flag_keywords"])
            creatures.append(creature)
        player.battlefield=creatures



    def env_no_mana(self,player):
        player.mana={"colorless":0,"U":0,"W":0,"B":0,"R":0,"G":0}
    def env_low_mana(self,player):
        player.mana={"colorless":1,"U":1,"W":1,"B":1,"R":1,"G":1}
        for key in player.mana:
            player.mana[key]+=random.randint(0,2)
    def env_middle_mana(self,player):
        player.mana={"colorless":2,"U":2,"W":2,"B":2,"R":2,"G":2}
        for key in player.mana:
            player.mana[key]+=random.randint(0,3)
        
    def env_high_mana(self,player):
        player.mana={"colorless":3,"U":3,"W":3,"B":3,"R":3,"G":3}
        for key in player.mana:
            player.mana[key]+=random.randint(0,5)

    def choose_card(self,constraint:dict):
        if constraint.get("battlefield",None):
            return self.get_cards_sample_by_name("creature",1)[0]
        if constraint.get("hand",None):
            return self.get_cards_sample_by_name("undo",1,True)[0]
        
        
    def sample_action(self,action_range:tuple[int,int]):
        # 从 mask 里抽一个为 true index，但是有范围限制
        
        actions_mask = self.create_action_mask_old(self.player_1)[0]
        print(actions_mask)
        min_index,max_index = action_range  # 设置你想要的最大index（不包含max_index本身）
        actions = [i for i in range(min_index, max_index) if actions_mask[i]]
        if not actions:
            return None
        action = random.choice(actions)
        return action

        
    
    def simulate_play(self):
        card_name=self.choose_card({"hand":True})
        card=CARD_DICTION[card_name](self.player_1)
        card.flag_dict["tap"]=False
        self.player_1.hand=[card]
        self.active_player=self.player_1
        self.non_active_player=self.player_2

        instance_dict={
            Creature:"when_enter_battlefield",
            Instant:"card_ability",
            Land:"when_enter_landarea",
            Sorcery:"card_ability"
        }
        select_dict={
            'all_roles':[self.player_2,self.player_1],
            'opponent_roles':[self.player_2], 
            'your_roles':[self.player_1],
            'all_creatures':[self.player_2,self.player_1],
            'opponent_creatures':[self.player_2],
            'your_creatures':[self.player_1],
        }
        
        for cls in instance_dict:
            if isinstance(card,cls):
                select_range=getattr(card,instance_dict[cls]).select_range
        if select_range in select_dict:
            for player in select_dict[select_range]:
                if not player.battlefield:
                    self.env_creature(player)
        elif "land" in select_range:
            return None


        action=self.sample_action((22,22+33))

        simulate_info={
            "card":card,
            "type":0,
            "action":action
        }

        return simulate_info
    

    def simulate_creature_attack(self):
        card_name=self.choose_card({"battlefield":True})
        card=CARD_DICTION[card_name](self.player_1)
        self.player_1.battlefield.append(card)
        
        card_index=len(self.player_1.battlefield)-1
        if card.get_flag("Double strike"):
            card.set_counter_dict("attack_counter",2)
        else:
            card.set_counter_dict("attack_counter",1)
        card.flag_dict["summoning_sickness"]=False
        card.flag_dict["tap"]=False
        self.flag_dict["attacker_defenders"]=False
        
        self.active_player=self.player_1
        self.non_active_player=self.player_2


        action=self.sample_action((2+card_index,2+card_index+1))

        simulate_info={
            "card":card,
            "type":1,
            "action":action
        }

        return simulate_info

    def simulate_creature_defend(self):
        self._elapsed_time=time.perf_counter()
        card_name=self.choose_card({"battlefield":True})
        card=CARD_DICTION[card_name](self.player_1)
        card.flag_dict["tap"]=False
        self.player_1.battlefield.append(card)
        card_index=len(self.player_1.battlefield)-1
        card.flag_dict["summoning_sickness"]=False
        self.flag_dict["attacker_defenders"]=True
        opponent_card=random.choice(self.player_2.battlefield)
        self.attacker=opponent_card
        self.active_player=self.player_2
        self.non_active_player=self.player_1


        action=self.sample_action((12+card_index,12+card_index+1))

        simulate_info={
            "card":card,
            "type":2,
            "action":action
        }
        return simulate_info

    async def action_process_system(self):#这个会等待，直到收到send_actioin_request发送的请求
        repeat_train=True
        while repeat_train:
            

            for i in range(256):
                simulate_info=self.change_environmrnt()
                print(self)
                print(simulate_info)
                action=simulate_info["action"]
                if action is None:
                    continue
                agent:Agent_Train=self.player_1
                state=self.get_new_state(agent)

                #print(action)
                reward_func=await self.process_action(agent,action)
                print(self)

                print("\n\n\n\n\n")
                #asyncio.create_task(agent.store_data(state,action,reward_func))
                
                #print(self)
                oppo_agent:Agent_Train=agent.opponent

                #print(agent.name,mask,action)
                if agent==self.player_1:
                    
                    if action!=0:
                        await agent.store_data(state,action,reward_func)
                    else:
                        #print("store_data_func",action)
                        
                        async def store_data_func(agent=agent,state=state,action=action,reward_func=reward_func):
                            #print("store_data_func",action,id(store_data_func),id(reward_func),id(state))
                            await agent.store_data(state,action,reward_func)
                        #print("store_data_func",action,id(store_data_func),id(reward_func),id(state))
                        agent.add_pedding_store_task(store_data_func)
                    
                await self.check_death()
                
            
            self.send_data_to_host(agent if agent==self.player_1 else oppo_agent)
            #print("finish")
            self.gamming=True
            await self.initinal_environmrnt()
            
            
        #self.active_player.update()

    def send_data_to_host(self,agent:Agent_Train):


        self.info_communication.store_game_data(agent.agent.dataset.datas)
        agent.agent.dataset.datas = []
    
        

    async def game_end(self,died_player:list[Agent_Train]):
        self.gamming=False
       
        for player in [self.player_1,self.player_2]:
            await player.clear_pedding_store_task()

    def get_new_state(self,agent:Agent_Train):
        state_batch={}

        basic_state=[]
        oppo_agent=agent.opponent

        self_life=max(0,min(20,int(agent.life)))
        self_life_one_hot=np.zeros(21)
        self_life_one_hot[self_life]=1
        state_batch["self_life"]=self_life_one_hot

        oppo_life=max(0,min(20,int(oppo_agent.life)))
        oppo_life_one_hot=np.zeros(21)
        oppo_life_one_hot[oppo_life]=1
        state_batch["oppo_life"]=oppo_life_one_hot
        max_mana=20
        self_mana=[]
        cost=self.get_cost_total(agent)
        for color in ["U","R","G","W","B"]:
            mana_cost=cost[color]
            mana_cost=max(0,min(max_mana,int(mana_cost)))
            # one_hot=np.zeros(max_mana)
            # one_hot[mana_cost]=1
            self_mana.append(mana_cost)
        

        state_batch["self_mana"]=self_mana

        
        card_types=[]
        card_special_types=[]
        card_costs=[]
        card_atks=[]
        card_hps=[]
        card_has_attack=[]
        card_has_defend=[]
        card_mask=[]
        
        length_hand=len(agent.hand)
        for hand_i in range(10):
            if hand_i <length_hand:
                card=agent.hand[hand_i]

                

                card_type,card_special_type=self.get_card_special_types(card)

                card_types.append(card_type)
                card_special_types.append(card_special_type)

                card_manas=[]
                for mana in list(card.calculate_cost().values()):
                    mana=max(0,min(max_mana,int(mana)))
                    # mana_one_hot=np.zeros(max_mana)
                    # mana_one_hot[mana]=1
                    card_manas.append(mana)
                #card_manas=np.concatenate(card_manas, axis=0)
                #print(card.calculate_cost().values())
                card_costs.append(np.array(card_manas))

                if card_type==1:
                    attack,defend=card.state
                    card_atks.append(attack)
                    card_hps.append(defend)
                    card_has_attack.append(1)
                    card_has_defend.append(1)
                else:
                    card_atks.append(0)
                    card_hps.append(0)
                    card_has_attack.append(0)
                    card_has_defend.append(0)

                card_mask.append(1)
            else:
                
                card_types.append(0)
                card_special_types.append(np.zeros(20))
                card_costs.append(np.zeros(6))
                card_atks.append(0)
                card_hps.append(0)
                card_has_attack.append(0)
                card_has_defend.append(0)
                card_mask.append(0)



        state_batch["self_board"]=self.get_creature_state_new_batch(agent,agent.battlefield)
        state_batch["oppo_board"]=self.get_creature_state_new_batch(agent,oppo_agent.battlefield)

        
        state_batch["simulate_state"]=0#0:play,1:attack,2:defend
        return state_batch


    async def process_action(self,agent:Agent_Train,action:int)->tuple:
        #将action 处理生成动作并且传入房间，将其挂起，直到房间处理好请求收到结束信号
        #如果是攻击的action，给敌方agent发送动作请求，自己挂起再一次，直到地方action动作做好发送信息给自己，自己结束挂起，计算state
        # 获取state，done，计算reward
        #返回new state 和 reward 和 done
        org_state=str(self)
        message:str=await self.num2action_old(agent,action)
        print(message)
        username,type,content=message.split("|")
        #old_reward=self.get_reward_red(agent)
        #print(username,content,type)
        old_rewards=self.reward_func[agent.name](agent)
        info_index=len(self.game_recorder[agent.name].datas)
        old_reward=old_rewards["reward"]

        if action==1 or (action>=12 and action <=21):
            attacker=self.attacker
            
        else:
            attacker=None
        if action>=2 and action <=21:
            print(agent.battlefield)
            print(content)
            
            selected_creature=agent.battlefield[int(content)]
        else:
            selected_creature=None
        await self.message_process_dict[type](username,content)
        await self.check_death()

        flag=False
        if action>=2 and action <=11:
            
            agent_oppo:Agent_Train=agent.opponent
            state=self.get_new_state(agent_oppo)
            mask=self.create_action_mask_old(agent_oppo)
            state["mask"]=mask
            action_oppo= 1
            await self.process_action(agent_oppo,action_oppo)

            
            
        
        elif action!=0:
            await self.end_bullet_time()
        elif action==0:
            # async def zero_reward_func():
            #     return state,0,False
            #agent.notify_reward=False

            flag=True

        
        #change_reward=new_reward-old_reward

        async def next_state_function(info_index=info_index):
            
            current_rewards=self.reward_func[agent.name](agent,selected_creature,attacker)
            current_reward=current_rewards["reward"]
            # if action==0:
            #     new_reward=0
            # else:
                
            new_reward=current_reward-old_reward
            new_reward/=5
            if action==0:
                info_index=len(self.game_recorder[agent.name].datas)
                new_reward/=50
            

            if self.config.get("long_sight",False):
                if action>=2 and action <=11:
                    new_reward=0
                if action==0:
                    new_reward=0
                #new_reward*=5
                
            new_reward=max(min(new_reward,0.3),-0.3)
            #await self.check_death()
            die_player=await self.check_player_die()
            
            done=False
            
            if die_player and agent.life<=0:
                
                new_reward=-1
                done=True

                #if flag:
                # print("lose",action,message,agent.life,org_state,self,self.gamming,new_reward)
                # print("traceback.format_stack():")
                # print("".join(traceback.format_stack()))
            elif die_player:
                
                new_reward=1
                done=True
                # print("win",action,message,agent.life,org_state,self,self.gamming,new_reward)
                # print("traceback.format_stack():")
                # print("".join(traceback.format_stack()))
            if action==1:
                done=False
            #print(message)
            await self.game_recorder[agent.name].store_game_reward(info_index,message,new_reward,old_rewards,current_rewards)
            
            return self.get_new_state(agent),new_reward,done,current_reward
        return next_state_function



async def run_parallel_room(config_path:str,config_path_list:list,info_communication:"Info_Communication",worker_id:int):
    
    room=Multi_Agent_Parallel_Specific_Room(
        config_path,
        config_path_list,
        info_communication,
        worker_id
    )
    
    await room.game_start()
    await room.action_process_system()

def worker_process(config_path:str, config_path_list:list, info_communication:"Info_Communication", worker_id:int):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    asyncio.run(
        run_parallel_room(
            config_path,
            config_path_list,
            info_communication,
            worker_id
        )
    )

if __name__=="__main__":

    print(Multi_Agent_Parallel_Specific_Room.get_cards_sample_by_name(None,"land",4,False))