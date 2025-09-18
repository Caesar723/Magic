if __name__=="__main__":
    import sys
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/src")
    
   
import inspect
import traceback
import random
#from room_server import RoomServer
import numpy as np
import asyncio
from game.train_agent import Agent_Train
from game.room import Room
from game.ppo_train import Agent_PPO
from game.rlearning.module.ppo_agent import PPOTrainer
from game.rlearning.utils.model import get_class_by_name

from game.card import Card
from game.type_cards.creature import Creature
from game.type_cards.instant import Instant
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery
from game.rlearning.utils.file import read_yaml
from game.base_agent_room import Base_Agent_Room
from game.game_recorder import GameRecorder





class Multi_Agent_Room(Base_Agent_Room):
    """
    当回合开始的时候，向那个活跃的agent发送做动作的请求
    做好一个动作之后把状态奖励等放入agent里
    直到agent 做出了 0:end turn的这个动作
    """

    def __init__(self,config_path:str) -> None:
        
        self.config_path=config_path
        
        self.config=read_yaml(config_path)
        

        trainer1=get_class_by_name(self.config["trainer"])
        trainer2=get_class_by_name(self.config["trainer"])
        
        self.agent1=trainer1(self.config,self.config["restore_step"],name="main")
        self.agent2=trainer2(self.config,self.config["restore_step"],name="AgentCompanion")
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

        

    def initinal_player(self,players:list[tuple],is_initinal:bool=True):
        agents_deck="Eternal Phoenix+Creature+4|Raging Firekin+Creature+4|Emberheart Salamander+Creature+4|Arcane Inferno+Instant+4|Pyroblast Surge+Instant+4|Fiery Blast+Instant+4|Inferno Titan+Creature+4|Flame Tinkerer+Creature+4|Mountain+Land+24"

        players=[(agents_deck,"Agent1"),(agents_deck,"AgentCompanion")]
        
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
        old_rewards=self.get_reward_attack(agent)
        info_index=len(self.game_recorder[agent.name].datas)
        old_reward=old_rewards["reward"]
        if action>=2 and action <=21:
            selected_creature=agent.battlefield[int(content)]
        else:
            selected_creature=None
        await self.message_process_dict[type](username,content)
        await self.check_death()

        flag=False
        #print(action)
        if action>=2 and action <=11:
            agent_oppo:Agent_Train=agent.opponent
            #print(agent_oppo.hand)
            state=self.get_new_state(agent_oppo)
            mask=self.create_action_mask(agent_oppo)
            state["mask"]=mask
            #print(mask)
            action_oppo= agent_oppo.choose_action(state,isTrain=True)
            #print(action)
            reward_func=await self.process_action(agent_oppo,action_oppo)

            if agent_oppo==self.player_1:
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
            current_rewards=self.get_reward_attack(agent,selected_creature)
            current_reward=current_rewards["reward"]
            # if action==0:
            #     new_reward=0
            # else:
                
            new_reward=current_reward-old_reward
            new_reward/=10
            if action==0:
                info_index=len(self.game_recorder[agent.name].datas)
                new_reward/=50
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
            await self.game_recorder[agent.name].store_game_reward(info_index,message,new_reward,old_rewards,current_rewards)
            return self.get_new_state(agent),new_reward,done,current_reward
        return next_state_function
        
    
   

        

    #将 (英雄的血量/20)+(（随从的血量/攻击力）/20)   -((英雄的血量/20)+(（随从的血量/攻击力）/20)) 因为是红色的注重与敌方的血量
    # 
    #还有法力值上限也需要考虑
    #reward 是上面奖励的变化量
    # def get_reward_attack(self,agent:Agent_Train):#返回一个评分
    #     # if agent.life<=0:
    #     #     return -1
    #     # elif agent.opponent.life<=0:
    #     #     return 1
    #     self_live_reward=lambda x :x/20#lambda x :1/(1+np.e**(4-x))#用于红色的公式，卖血
    #     oppo_live_reward=lambda x :x/20

    #     score_life_self=self_live_reward(agent.life)
    #     score_oppo_self=oppo_live_reward(agent.opponent.life)

    #     score_battle_self=sum([sum(card.state)/10 for card in agent.battlefield])#这个处以20表面随从不是很重要，重要的是敌方的血量
    #     score_battle_oppo=sum([sum(card.state)/10 for card in agent.battlefield])

    #     score_mana=0
    #     for land in agent.land_area:
    #         score_mana+=sum(land.generate_mana().values())
    #     score_mana=score_mana/20

    #     return (score_life_self-score_oppo_self)+score_mana+score_battle_self-score_battle_oppo

    # def get_reward_life(self,agent:Agent_Train):#返回一个评分
    #     # if agent.life<=0:
    #     #     return -1
    #     # elif agent.opponent.life<=0:
    #     #     return 1
    #     self_live_reward=lambda x :x/20#lambda x :1/(1+np.e**(4-x))#用于红色的公式，卖血
    #     oppo_live_reward=lambda x :x/40

    #     score_life_self=self_live_reward(agent.life)
    #     score_oppo_self=oppo_live_reward(agent.opponent.life)

    #     score_battle_self=sum([sum(card.state)/10 for card in agent.battlefield])#这个处以20表面随从不是很重要，重要的是敌方的血量
    #     score_battle_oppo=sum([sum(card.state)/10 for card in agent.battlefield])

    #     score_mana=0
    #     for land in agent.land_area:
    #         score_mana+=sum(land.generate_mana().values())
    #     score_mana=score_mana/20

    #     return (score_life_self-score_oppo_self)+score_mana+score_battle_self-score_battle_oppo






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
                #print(len(agent.agent.reward),len(oppo_agent.agent.reward))
                # if len(agent.agent.reward)>=1024 and len(oppo_agent.agent.reward)>=1024:
                #     print("____________________update agent____________________")
                #     agent.update()
                #     oppo_agent.update()
                #     break
                if agent==self.player_1:
                    is_update=agent.update()
                    if is_update:
                        self.update_flag[agent.name]=True
                        
                else:
                    is_update=oppo_agent.update()
                    if is_update:
                        self.update_flag[oppo_agent.name]=True
                
                
            #print("finish")
            self.gamming=True
            await self.initinal_environmrnt()
            self.player_2.agent.restore_checkpoint(self.get_random_restore_step())
            
            
        #self.active_player.update()
    def get_random_restore_step(self):
        save_step=self.config["save_step"]
        max_restore=max(int(self.player_1.agent.step//save_step)-1,0)
        random_restore=random.randint(0,max_restore)
        return random_restore*save_step
        

    async def game_end(self,died_player:list[Agent_Train]):
        self.gamming=False
        
        for player in [self.player_1,self.player_2]:
            await player.clear_pedding_store_task()
        



        





            

    



















from game.buffs import StateBuff
async def tasks(room):
    await asyncio.sleep(6)
    for name in room.players:
        room.players[name].draw_card(2)
        print("draw cards")
        print(room.action_store_list_cache)
    #asyncio.create_task(room.message_receiver("t|play_card|1"))
async def main():
    
    room=Multi_Agent_Room(
        "/Users/xuanpeichen/Desktop/code/python/openai/src/game/rlearning/config/white/ppo_lstm2.yaml",
    )
    
    await room.game_start()
    await room.action_process_system()
    # print(room.get_new_state(room.player_1))
    # print("\n\n".join([i.text(room.player_1) for i in room.player_1.hand]))
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
