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

from game.train_agent import Agent_Train 
from game.rlearning.utils.model import get_class_by_name
from game.rlearning.utils.file import read_yaml
from game.base_agent_room import Base_Agent_Room
from game.game_recorder import GameRecorder
from game.rlearning.utils.agentSchedule import AgentSchedule
from initinal_file import ORGPATH
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.communicate.training_parallel_room import Info_Communication



class Multi_Agent_Parallel_Room(Base_Agent_Room):
    """
    当回合开始的时候，向那个活跃的agent发送做动作的请求
    做好一个动作之后把状态奖励等放入agent里
    直到agent 做出了 0:end turn的这个动作
    """

    def __init__(self,
    env_config,
    info_communication:"Info_Communication",
    worker_id:int,
    ) -> None:
        self.env_config=env_config
        config_path=f"{ORGPATH}/{env_config['agent_config']}"
        config_path_list=[f"{ORGPATH}/{config_path}" for config_path in env_config["opponent_config"]]
        self.info_communication=info_communication
        self.worker_id=worker_id
        
        self.config_path=config_path
        self.config_path_list=config_path_list
        self.config=read_yaml(config_path)
        self.config_list=[read_yaml(config_path) for config_path in config_path_list]

        trainer1=get_class_by_name(self.config["trainer"])
        trainer1.pbar=None
        trainer_list=[get_class_by_name(config["trainer"]) for config in self.config_list]
        
        self.agent1=trainer1(self.config,self.config["restore_step"],name="main")
        self.agent_list={
            config_path_list[i]:trainer(self.config_list[i],self.config_list[i]["restore_step"],name=f"agent{i+1}") 
            for i,trainer in enumerate(trainer_list)
        }
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

        
        

        

    def initinal_player(self,players:list[tuple],is_initinal:bool=True):
        agents_deck="Eternal Phoenix+Creature+4|Raging Firekin+Creature+4|Emberheart Salamander+Creature+4|Arcane Inferno+Instant+4|Pyroblast Surge+Instant+4|Fiery Blast+Instant+4|Inferno Titan+Creature+4|Flame Tinkerer+Creature+4|Mountain+Land+24"

        model_info= self.info_communication.get_model_info(self.worker_id)
        print(model_info)

        players=[(agents_deck,"Agent1"),(agents_deck,"Agent2")]
        
        self.player_1=Agent_Train(players[0][1],self,self.agent1)
        self.player_1.agent.pbar=None
        
        agent_oppo=self.agent_list[model_info["config_opponent_path"]]
        self.player_2=Agent_Train(players[1][1],self,agent_oppo)
        
        self.player_1.set_opponent_player(self.player_2,self)
        self.player_2.set_opponent_player(self.player_1,self)

        for treasure in self.agent1.config.get("treasures",[]):
            class_treasure=get_class_by_name(treasure)
            self.player_1.treasure.append(class_treasure())
            
        for treasure in agent_oppo.config.get("treasures",[]):
            class_treasure=get_class_by_name(treasure)
            self.player_2.treasure.append(class_treasure())

        self.player_1.change_function_by_treasure()
        self.player_2.change_function_by_treasure()

        self.players:dict[Agent_Train]={
            players[0][1]:self.player_1,
            players[1][1]:self.player_2
        }

        self.players_socket:dict={
            players[0][1]:None,
            players[1][1]:None
        }

        
        #print(self.update_flag)
        if is_initinal:
        
            self.update_flag:dict[bool]={
                self.player_1.name:False,
                self.player_2.name:False
            }
            #print(record_flag)
            self.game_recorder:dict["GameRecorder"]={
                players[0][1]:GameRecorder(self.player_1,self),
                players[1][1]:GameRecorder(self.player_2,self)
            }

        

        self.reward_func:dict[str,function]={
            players[0][1]:self.reward_dict[self.config.get("reward_type","reward_balance")],
            players[1][1]:self.reward_dict[self.config.get("reward_type","reward_balance")]
        }
        #print(self.reward_func)

        
        if model_info["success_update"]:
            self.update_flag[self.player_1.name]=True
            self.player_1.agent.restore_checkpoint(model_info["model_path"])
        if model_info["success_opponent_update"]:
            self.player_2.agent.restore_checkpoint(model_info["model_opponent_path"])
        #self.player_2.agent.restore_checkpoint(AgentSchedule.get_restore_step(self.player_2))

    # def get_random_restore_step(self,agent:Agent_Train):
    #     save_step=agent.agent.config["save_step"]
    #     max_restore=max(int(agent.agent.max_step//save_step)-1,0)
    #     random_restore=random.randint(0,max_restore)
    #     return random_restore*save_step

    def get_random_restore_step(self,agent:Agent_Train):
        logdir=agent.agent.logdir
        paths=[path.split("_")[1].split(".")[0] for path in os.listdir(os.path.join(logdir,"ckpt")) if path.startswith("config")]
        random_restore=random.choice(paths)
        return random_restore
       

    
    

    async def process_action(self,agent:Agent_Train,action:int)->tuple:
        #将action 处理生成动作并且传入房间，将其挂起，直到房间处理好请求收到结束信号
        #如果是攻击的action，给敌方agent发送动作请求，自己挂起再一次，直到地方action动作做好发送信息给自己，自己结束挂起，计算state
        # 获取state，done，计算reward
        #返回new state 和 reward 和 done
        org_state=str(self)
        message:str=await self.num2action(agent,action)
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
            selected_creature=agent.battlefield[int(content)]
        else:
            selected_creature=None
        await self.message_process_dict[type](username,content)
        await self.check_death()

        flag=False
        if action>=2 and action <=11:
            
            agent_oppo:Agent_Train=agent.opponent
            state=self.get_new_state(agent_oppo)
            mask=self.create_action_mask(agent_oppo)
            state["mask"]=mask
            action_oppo= agent_oppo.choose_action(state,isTrain=True)
            #print(action)
            reward_func=await self.process_action(agent_oppo,action_oppo)

            
            if agent_oppo==self.player_1 and np.sum(mask)!=1:
                if action_oppo!=0:
                    await agent_oppo.store_data(state,action_oppo,reward_func)
                else:
                    async def store_data_func():
                        
                        await agent_oppo.store_data(state,action_oppo,reward_func)
                    agent_oppo.add_pedding_store_task(store_data_func)

            
        
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
                state=self.get_new_state(agent)
                mask=self.create_action_mask(agent)
                state["mask"]=mask
                action=agent.choose_action(state,isTrain=True)
                #print(action)
                reward_func=await self.process_action(agent,action)
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
                
            if agent==self.player_1:
                self.send_data_to_host(agent)
                
                    
            else:
                self.send_data_to_host(oppo_agent)
                
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


async def run_parallel_room(config_path:str,config_path_list:list,info_communication:"Info_Communication",worker_id:int):
    
    room=Multi_Agent_Parallel_Room(
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