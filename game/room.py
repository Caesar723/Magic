if __name__=="__main__":
    import sys
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/")
    
    






import asyncio
import random
import time



from game.player import Player
from game.action import Action
from game.type_action import actions
from game.card import Card





class Room:
    
    
    def __init__(self,players:list[tuple]) -> None:#((deck,user_name1),...)
        self.gamming=True #如果在游戏的话就是True，没有就是False

        #used to store all action
        self.action_store_list_cache:list[Action]=[]#先存cache 然后转移给list，cache清空
        self.action_store_list:list[Action]=[]

        #used to count the time for a turn
        self.turn_timer:int=0
        self.max_turn_time:int=60

        #used to count the time when player use instant and in bullet_time
        self.bullet_timer:int=0
        self.max_bullet_time:int=5

        # used to store the players
        self.player_1,self.player_2=Player(players[0][1],players[0][0],self.action_store_list_cache),\
                                    Player(players[1][1],players[1][0],self.action_store_list_cache)
        self.player_1.set_opponent_player(self.player_2)
        self.player_2.set_opponent_player(self.player_1)
        self.players:dict={
            players[0][1]:self.player_1,
            players[1][1]:self.player_2
        }

        #用来发送消息
        self.players_socket:dict={
            players[0]:None,
            players[1]:None
        }


        #used to store the each flag like whether is bullet_time
        self.flag_dict:dict={}

        #used to store each counter like number of turns
        self.counter_dict:dict={}

        #store current player which is in his turn
        self.active_player:Player#进行操作的玩家
        self.non_active_player:Player

        #stack
        self.stack:list[tuple]=[]#(preparend_function,card) 这个很重要

        #attacker
        self.attacker:Card=None

        #defenders
        self.defenders:list[Card]=None


        self.message_process_dict={
            "select_attacker":self.select_attacker,
            "select_defender":self.select_defender,
            "play_card":self.play_card,
            "end_step":self.end_step,
            "discard":self.discard,
            "activate_ability":self.activate_ability,
            "concede":self.concede,
            "end_bullet_time":self.end_bullet_time

        }
        self.message_process_condition=asyncio.Condition()#当list是空的时候就会调用这个，让程序有序运行
        self.message_process_queue=[]

        #start executing message_process
        asyncio.create_task(self.message_process())

    
    async def game_start(self):# start the game
        players=[self.player_1,self.player_2]
        player1=random.choice(players)
        players.remove(player1)
        player2=players[0]
        
        self.active_player=player1
        self.non_active_player=player2
        asyncio.create_task(self.timer_task())

        self.flag_dict["bullet_time"]=False
        self.flag_dict["attacker_defenders"]=False
        self.reset_turn_timer()
        

    def start_attack(self):# attacker and defenders start attack
        pass

    async def update_timer(self):# update turn_timer and bullet_time_timer
        self.turn_timer:int=self.max_turn_time-round(time.perf_counter()-self.initinal_turn_timer)
        print(self.turn_timer)
        if self.turn_timer<=0:
            await self.end_turn_time()

        if self.flag_dict["bullet_time"]:
            self.bullet_timer:int=self.max_bullet_time-round(time.perf_counter(),self.initinal_bullet_timer)
            if self.bullet_timer<=0:
                await self.end_bullet_time()
        

    def end_turn_time(self):#turn_timer is 0
        self.change_turn()
        self.reset_turn_timer()

    def end_bullet_time(self):#bullet_time is 0
        if self.flag_dict["attacker_defenders"]:
            pass#让cards 进行攻击阻挡
            self.flag_dict["attacker_defenders"]=False
        #self.stack 用pop(0)把每一个函数调用
        self.reset_bullet_timer(self)


    def reset_turn_timer(self):
        self.initinal_turn_timer=time.perf_counter()
        self.action_store_list_cache.append(actions.Turn(self.active_player,self.active_player,True))
        

    def reset_bullet_timer(self):
        self.initinal_bullet_timer=time.perf_counter()


    def change_turn(self):# when active_player end turn
        self.active_player,self.non_active_player=self.non_active_player,self.active_player
        #触发一些回合开始的东西

    

    async def message_receiver(self,message:str):# process all message
        """
        username|type|content

        ...|select_attacker|index
        ...|select_defender|index
        ...|play_card|index(在手牌的index)
        ##...|select_object|
        ...|end_step|
        ...|discard|[list of numbers]
        ...|activate_ability|区域;index
        ...|concede(投降)|
        ...|end_bullet_time|...
        
        """
        username,type,content=message.split("|")
        if type in self.message_process_dict:
            async with self.message_process_condition:
                self.message_process_queue.append((self.message_process_dict[type],(username,content)))
                self.message_process_condition.notify()  # 通知等待的协程条件已满足
            

    async def message_process(self):# 为了让每一个步骤变得有序
        while self.gamming:
            if not self.message_process_queue:
                async with self.message_process_condition:
                    await self.message_process_condition.wait_for(lambda: len(self.message_process_queue) > 0)  # 等待队列不为空
            func=self.message_process_queue.pop(0)
            await func[0](*func[1]) 

    async def select_attacker(self,username:str,content:str):
        player:Player=self.players[username]
        if player==self.active_player:
            player.select_attacker(int(content))
            return (True,"success")# bool, reason
        else:
            return (False,"You must do it in your turn")

    async def select_defender(self,username:str,content:str):
        player:Player=self.players[username]
        if player==self.active_player:
            player.select_defender(int(content))
            return (True,"success")
        else:
            return (False,"You must do it in your turn")

    async def play_card(self,username:str,content:str):
        player:Player=self.players[username]
        index=int(content)
        card=player.get_card_index(index,"hand")
        
        if player==self.active_player:# 如果card 的类型是instant，可以直接释放
            player.play_a_card(card)
            return (True,"success")
        else:
            return (False,"You must do it in your turn")

    async def end_step(self,username:str,content:str):
        player:Player=self.players[username]
        if player==self.active_player:
            self.end_turn_time()
            return (True,"success")
        else:
            return (False,"You must attack in your turn")

    async def discard(self,username:str,content:str):
        pass

    async def end_bullet(self,username:str,content:str):
        player:Player=self.players[username]
        if player==self.active_player:
            self.end_bullet_time()
            return (True,"success")
        else:
            return (False,"You must attack in your turn")


    async def activate_ability(self,username:str,content:str):
        pass

    async def concede(self,username:str,content:str):
        pass

    def set_socket(self,socket,username:str):#用来初始化socket
        self.players_socket[username]=socket

    async def timer_task(self):# 每一秒 更新时间
        while self.gamming:
            print("update_timer")
            await asyncio.sleep(0.5)
            await self.update_timer()
            
            
if __name__=="__main__":
    async def main():
        test="Mystic Tides+Instant+1|Mystic Reflection+Instant+1|Mystic Evasion+Instant+2|Mindful Manipulation+Sorcery+1|Nyxborn Serpent+Creature+1|Mistweaver Drake+Creature+1"
        room=Room([(test,"1"),(test,"2")])
        await room.game_start()
        room.active_player=room.players["1"]
        room.non_active_player=room.players["2"]
        
        await room.message_receiver("1|play_card|0")
        await asyncio.sleep(5)
    asyncio.run(main())
    
    

