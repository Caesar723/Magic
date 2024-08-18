if __name__=="__main__":
    import sys
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/")
    
    






import asyncio
import random
import time
from typing import Union,TYPE_CHECKING
if TYPE_CHECKING:
    from fastapi import WebSocket
    from game.room_server import RoomServer


from game.player import Player
#from game.action import Action
from game.type_action import actions
from game.card import Card
from game.type_cards.instant import Instant
from game.type_cards.creature import Creature
from game.type_cards.land import Land

from pycards.land.Mountain.model import Mountain
from pycards.land.Swamp.model import Swamp
from pycards.land.Plains.model import Plains
from pycards.land.Forest.model import Forest
from pycards.land.Island.model import Island
import game.custom_print


class Room:
    
    
    def __init__(self,players:list[tuple],room_server:"RoomServer") -> None:#((deck,user_name1),...)
        print(players)
        self.room_server=room_server #room_server可以用来删除room 和更新用户的任务

        self.gamming=True #如果在游戏的话就是True，没有就是False

        #used to store all action
        self.action_store_list_cache_condition=asyncio.Condition()#当list是空的时候就会调用这个，让程序有序运行
        self.action_store_list_cache:list[actions.List_Action]=[]#先存cache,cache 里存list of action 然后转移给list，拆开list，cache清空
        self.action_processor=actions.List_Action_Processor(self.action_store_list_cache,self.action_store_list_cache_condition)
        self.action_store_list:list[actions.Action]=[]

        #used to count the time for a turn
        self.turn_timer:int=0
        self.max_turn_time:int=60

        #used to count the time when player use instant and in bullet_time
        self.bullet_timer:int=0
        self.max_bullet_time:int=10

        self.initinal_player(players)
        #print(self.players_socket)

        #used to store the each flag like whether is bullet_time
        self.flag_dict:dict={}

        #used to store each counter like number of turns
        self.counter_dict:dict={}

        #store current player which is in his turn
        self.active_player:Player#进行操作的玩家
        self.non_active_player:Player

        #stack
        self.stack:list[tuple]=[]#(preparend_function,card) 这个很重要 card 是英文需要检查card 的类型

        #attacker
        self.attacker:Creature=None

        #defenders
        #self.defenders:list[Card]=None


        


        self.message_process_dict={
            "select_attacker":self.select_attacker,
            "select_defender":self.select_defender,
            "play_card":self.play_card,
            "end_step":self.end_step,
            "discard":self.discard,
            "activate_ability":self.activate_ability,
            "concede":self.concede,
            "end_bullet":self.end_bullet,
            "close_game":self.close_game

        }
        self.message_process_condition=asyncio.Condition()#当list是空的时候就会调用这个，让程序有序运行
        self.message_process_queue=[]

        #start executing message_process
        asyncio.create_task(self.message_process())
        asyncio.create_task(self.action_sender())


        
        
    def initinal_player(self,players:list[tuple]):
        # used to store the players
        self.player_1,self.player_2=Player(players[0][1],players[0][0],self.action_processor),\
                                    Player(players[1][1],players[1][0],self.action_processor)
        self.player_1.set_opponent_player(self.player_2,self)
        self.player_2.set_opponent_player(self.player_1,self)
        self.players:dict[Player]={
            players[0][1]:self.player_1,
            players[1][1]:self.player_2
        }

        #用来发送消息
        
        self.players_socket:dict["WebSocket"]={
            players[0][1]:None,
            players[1][1]:None
        }
    
    async def game_start(self):# start the game
        players=[self.player_1,self.player_2]
        player1=random.choice(players)
        players.remove(player1)
        player2=players[0]
        
        self.active_player:Player=player1
        self.non_active_player:Player=player2
        asyncio.create_task(self.timer_task())

        # self.flag_dict["bullet_time"]=False
        # self.flag_dict["attacker_defenders"]=False
        self.reset_turn_timer()

        #######test
        #print("发送消息")
        #asyncio.create_task(tasks(self))
        # asyncio.run(main())


    #finish game 给客户发送胜利/失败的消息。
    #关闭socket，gaming=false，
    #把两个player交给room server，用来收集任务进度，
    #最后room server把房间移除，玩家移除
    #
    async def game_end(self,died_player:list[Player]):
        #self.gamming=False

        self.action_processor.start_record()
        if len(died_player)==2:
            for player in died_player:
                self.action_processor.add_action(actions.Lose(player,player))
                #await self.room_server.settle_player(False,player)
        else:
            lose_player=died_player[0]
            win_player=lose_player.opponent
            self.action_processor.add_action(actions.Win(win_player,win_player))
            self.action_processor.add_action(actions.Lose(lose_player,lose_player))
            #await self.room_server.settle_player(True,win_player)
            #await self.room_server.settle_player(False,lose_player)
        self.action_processor.end_record()
        #print(self.action_processor.action_cache)

        

    async def start_attack(self,defender:Union[Creature,Player]):# attacker and defenders start attack
        self.action_processor.start_record()
        if isinstance(defender,Creature):
            self.attacker.when_start_attcak(defender,self.attacker.player,self.attacker.player.opponent)
            defender.when_start_defend(self.attacker,defender.player,defender.player.opponent)
            rest_live=await self.attacker.deal_damage(defender,self.attacker.player,self.attacker.player.opponent)
            await defender.deal_damage(self.attacker,defender.player,defender.player.opponent)
            state_attacker=self.attacker.state
            state_defender=defender.state
            self.action_processor.add_action(actions.Creature_Start_Attack(self.attacker,self.attacker.player,defender,False,state_attacker,state_defender))

            if self.attacker.get_flag("Trample") and rest_live<0:
            #opponent.take_damage(self,abs(rest_live))
                self.action_processor.start_record()
                await self.attacker.attact_to_object(self.attacker.player.opponent,int(abs(rest_live)),"rgba(243, 243, 243, 0.9)","Missile_Hit")
                self.action_processor.end_record()
            


        elif isinstance(defender,Player):
            self.attacker.when_start_attcak(defender,self.attacker.player,self.attacker.player.opponent)
            await self.attacker.deal_damage_player(defender,self.attacker.player,self.attacker.player.opponent)
            state_attacker=self.attacker.state
            self.action_processor.add_action(actions.Creature_Start_Attack(self.attacker,self.attacker.player,self.attacker.player.opponent,False,state_attacker,[self.attacker.player.opponent.life]))

        #self.attacker=None
        self.action_processor.end_record()

    def get_flag(self,flag_name:str):
        
        if flag_name in self.flag_dict:
            
            return self.flag_dict[flag_name]
        else:
            return False

    
    async def update_timer(self):# update turn_timer and bullet_time_timer
        if self.get_flag("bullet_time"):
            self.bullet_timer:int=self.max_bullet_time-round(time.perf_counter()-self.initinal_bullet_timer)
            await self.check_timer_change("timer_bullet",self.bullet_timer)
            #print(self.bullet_timer)
            if self.bullet_timer<=0:
                await self.end_bullet_time()
        else:
            #self.initinal_turn_timer-=round(time.perf_counter()-self.initinal_turn_timer)
            self.turn_timer:int=self.max_turn_time-round(time.perf_counter()-self.initinal_turn_timer)
            await self.check_timer_change("timer_turn",self.turn_timer)
            if self.turn_timer<=0:
                await self.end_turn_time()

        

    async def check_timer_change(self,name,time):
        #print("check",time)
        if not (name in self.counter_dict):
            self.counter_dict[name]=-1
        if self.counter_dict[name]!=time:
            self.counter_dict[name]=time
            for name_player in self.players_socket:
                socket:"WebSocket"=self.players_socket[name_player]
                if socket!=None:
                    await socket.send_text(f"{name}({time})")
                    

        

    async def end_turn_time(self):#turn_timer is 0
        #self.non_active_player.
        self.action_processor.start_record()
        await self.change_turn()
        self.reset_turn_timer()
        self.action_processor.end_record()
        

    async def end_bullet_time(self):#bullet_time is 0
        self.bullet_timer=0
        self.flag_dict["bullet_time"]=False
        await self.check_timer_change("timer_bullet",self.bullet_timer)
        self.initinal_turn_timer+=time.perf_counter()-self._elapsed_time

        for name_player in self.players_socket:
            socket:"WebSocket"=self.players_socket[name_player]
            if socket!=None:
                await socket.send_text("end_bullet()")

        key="{}_bullet_time_flag"
        for un in self.players:#username
            self.flag_dict[key.format(un)]=False
        #print(self.stack)
        while self.stack and not self.flag_dict["bullet_time"]:
            func,card=self.stack.pop()
            self.action_processor.start_record()
            #print(func,card,self.attacker)
            self.action_processor.start_record()
            self.action_processor.add_action(actions.Play_Cards(card,card.player))
            self.action_processor.end_record()
            result=await func()
            
            self.action_processor.end_record()
            if result=="defender" and isinstance(card,Creature) :

                await card.check_dead()
                await self.attacker.check_dead()

                #if not card.get_flag("die") and not self.attacker.get_flag("die"):#如果是有Menace 就记数，有两个defender才会让attacker_defenders变false 
                if not (card.get_flag("die") or self.attacker.get_flag("die") or card.get_flag("exile") or self.attacker.get_flag("exile")):
                    max_defender_number=1
                    self.add_counter_dict("defender_number",1)
                    if self.counter_dict["defender_number"]>=max_defender_number:
                        self.flag_dict["attacker_defenders"]=False
                        self.counter_dict["defender_number"]=0
                    
                    await self.start_attack(card)
            

        #self.stack 用pop()把每一个函数调用
        if not self.flag_dict["bullet_time"]:
            self.reset_bullet_timer()

            if self.get_flag("attacker_defenders"):#如果attacker_defenders还是True 那attacker 就去攻击敌方英雄
                await self.start_attack(self.non_active_player)
                self.flag_dict["attacker_defenders"]=False
                #print(self.flag_dict["attacker_defenders"])
            await self.check_death()
            #print(self.attacker)
            if self.attacker:
                self.action_processor.start_record()
                self.attacker.tap()
                self.action_processor.end_record()
            self.attacker=None
            

        


    def reset_turn_timer(self):
        self.initinal_turn_timer=time.perf_counter()
        self.action_processor.start_record()
        self.action_processor.add_action(actions.Turn(self.active_player,self.active_player))
        self.action_processor.end_record()

    def reset_bullet_timer(self):
        self.initinal_bullet_timer=time.perf_counter()

    async def start_bullet_time(self):
        #print("start_bullet()1")
        self.reset_bullet_timer()
        self.flag_dict["bullet_time"]=True
        self._elapsed_time=time.perf_counter()
        for name_player in self.players_socket:
            socket:"WebSocket"=self.players_socket[name_player]
            if socket!=None:
                await socket.send_text("start_bullet()")
        #print("start_bullet()")


    async def change_turn(self):# when active_player end turn
        await self.active_player.ending_phase()
        await self.active_player.cancel_future_function()
        await self.non_active_player.cancel_future_function()
        self.active_player,self.non_active_player=self.non_active_player,self.active_player
        
        await self.active_player.beginning_phase()
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
        ...|activate_ability|区域;index   #大部分是用在land，点击land激活能力产生法力
        ...|concede(投降)|
        ...|end_bullet|...#当两个玩家都end bullet time 的时候，他们才会真正的结束bullet time
        ...|start_attack|#当敌方用start_attack才有用
        ...|close_game|win or lose
       
        
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
            await self.check_death()

    async def select_attacker(self,username:str,content:str):
        player:Player=self.players[username]
        index=int(content)
        card:Creature=player.get_card_index(index,"battlefield")

        if not card:
            return (False,"no card")

        if player==self.active_player and not self.get_flag('attacker_defenders') and\
        (not card.get_flag("summoning_sickness") or card.get_flag("haste")) and\
        not card.get_flag("tap"):
            self.action_processor.start_record()
            self.action_processor.add_action(actions.Creature_Prepare_Attack(card,player))
            player.select_attacker(card)
            self.flag_dict['attacker_defenders']=True
            self.attacker=card
            card.when_become_attacker(player,player.opponent)
            await self.start_bullet_time()
            self.action_processor.end_record()
            
            return (True,"success")# bool, reason
        else:
            return (False,"You must do it in your turn")

    async def select_defender(self,username:str,content:str):
        player:Player=self.players[username]
        index=int(content)
        card:Creature=player.get_card_index(index,"battlefield")
        #print(card)
        if not card:
            return (False,"no card")
        print(player==self.non_active_player,self.get_flag("attacker_defenders"),not card.get_flag("tap"),(not self.attacker.get_flag("flying") or (card.get_flag("flying") or card.get_flag("reach"))))
        if player==self.non_active_player and \
        self.get_flag("attacker_defenders") and\
        not card.get_flag("tap") and \
        (not self.attacker.get_flag("flying") or (card.get_flag("flying") or card.get_flag("reach")))and \
        self.check_landwalk(self.attacker,player):
            self.action_processor.start_record()
            self.action_processor.add_action(actions.Creature_Prepare_Defense(card,player,self.attacker,False))
            player.select_defender(card)
            async def prepared_function():
                return "defender"
            #prepared_function=lambda: "defender"
            await self.put_prepared_function_to_stack(prepared_function,card)
            card.when_become_defender(player,player.opponent)
            self.action_processor.end_record()
            return (True,"success")
        else:
            return (False,"You must do it in your turn")
        
    def check_landwalk(self,card:Card,player:Player):
        walk_dict={
            "Islandwalk":Island,
            "Swampwalk":Swamp,
            "Forestwalk":Forest,
            "Mountainwalk":Mountain,
            "Plainswalk":Plains
        }
        for key in walk_dict:
            if card.get_flag(key) and any(isinstance(land,walk_dict[key]) for land in player.land_area):
                return True
            elif card.get_flag(key):
                return False
        return True

    


    async def play_card(self,username:str,content:str):
        player:Player=self.players[username]
        index=int(content)
        card:Card=player.get_card_index(index,"hand")
        
        if not card:
            return (False,"no card")
        if (player==self.active_player and not self.get_flag("bullet_time")) or isinstance(card,Instant) or card.get_flag("Flash"):# 如果card 的类型是instant，可以直接释放,或者card有flash
            return await self.start_play_card(card,player)
        else:
            return (False,"You must do it in your turn")
        
    async def start_play_card(self,card:"Card",player:Player):
        result=await player.play_a_card(card)
        #print(result)
        if result[0]:
            await self.put_prepared_function_to_stack(result[1],card)
        else:
            return result
    
    
    async def end_step(self,username:str,content:str):
        player:Player=self.players[username]
        if player==self.active_player:
            await self.end_turn_time()
            return (True,"success")
        else:
            return (False,"You must attack in your turn")

    async def discard(self,username:str,content:str):
        pass

    async def end_bullet(self,username:str,content:str):
        key="{}_bullet_time_flag"
        #player:Player=self.players[key.format(username)]
        self.flag_dict[key.format(username)]=True

        start=True

        
        socket:"WebSocket"=self.players_socket[username]
        if socket!=None:
            await socket.send_text("end_bullet()")

        for un in self.players:#username
            if not self.get_flag(key.format(un)):
                start=False
        if start:
            
            await self.end_bullet_time()
        
        return (True,"success")
        


    async def activate_ability(self,username:str,content:str):
        area,index=content.split(";")
        player:Player=self.players[username]
        index=int(index)
        card=player.get_card_index(index,area)
        
        if not card:
            return (False,"no card")
        
        if isinstance(card,Land) or card.check_can_use(player):# 如果card 的类型是instant，可以直接释放,或者card有flash
            self.action_processor.start_record()
            #self.action_processor.add_action(actions.Activate_Ability(card,player))
            await card.when_clicked(player,player.opponent)
            self.action_processor.add_action(actions.Change_Mana(card,player,player.get_manas()))

            self.action_processor.end_record()

        else:
            return (False,"You can't activate ability")
        
    async def close_game(self,username:str,content:str):
        player:Player=self.players[username]
        socket:"WebSocket"=self.players_socket[username]
        player.flag_dict["game_over"]=True

        try:
            await socket.close()
        except:pass

        if content=='win':
            await self.room_server.settle_player(True,player)
        elif content=='lose':
            await self.room_server.settle_player(False,player)
        #print(player.opponent.get_flag("game_over"),player.get_flag("game_over"))
        if player.opponent.get_flag("game_over"):
            self.gamming=False


    async def concede(self,username:str,content:str):
        pass

    async def set_socket(self,socket:"WebSocket",username:str):#用来初始化socket
        
        self.players_socket[username]=socket
        #print(f"set socket {username} {self.players_socket}")
        player=self.players[username]
        #print(self.text(player))
        await socket.send_text(self.text(player))

    def set_select_socket(self,socket:"WebSocket",username:str):
        self.players[username].socket_select_object=socket
        self.players[username].socket_connected_flag=True
        return self.players[username]

    async def timer_task(self):# 每一秒 更新时间
        while self.gamming:
            #print("update_timer")
            await asyncio.sleep(0.5)
            await self.update_timer()
            
    async def put_prepared_function_to_stack(self,prepared_function,card:Card):
        
        await self.start_bullet_time()
        self.stack.append((prepared_function,card))


    def add_counter_dict(self,key:str,number:int)->None:# change the numebr of counter_dict
        if key in self.counter_dict:
            self.counter_dict[key]+=number
        else:
            self.counter_dict[key]=number

    async def check_death(self):
        died_player=[]
        self.action_processor.start_record()
        for name in self.players:
            if (await self.players[name].check_dead()):
                died_player.append(self.players[name])

            for creature in self.players[name].battlefield.copy():
                await self.players[name].check_creature_die(creature)
        self.action_processor.end_record()
        if (died_player):
            #print(died_player)
            await self.game_end(died_player)

    async def action_sender(self):
        while self.gamming:
            #print("action_sender 检查一次")
            if not self.action_store_list_cache:
                
                async with self.action_store_list_cache_condition:
                    await self.action_store_list_cache_condition.wait_for(lambda: len(self.action_store_list_cache) > 0)  # 等待队列不为空
            #print(self.action_store_list_cache)
            action:actions.List_Action=self.action_store_list_cache.pop(0)
            self.action_store_list+=action.list_action
            
            await self.send_action(action)
            

            
            # await func[0](*func[1]) 
            # await self.check_death()
    async def send_action(self,action:actions.List_Action):
        #print(self.players_socket)
        for name in self.players_socket:
            player:Player=self.players[name]
            #print(player.name)
            socket:"WebSocket"=self.players_socket[name]
            if socket!=None:
                print("准备发送",action)
                try:
                    await socket.send_text(action.text(player))
                except:
                    pass
                print("发送成功")

    # async def selection_process_queue(self):
    #     while self.gamming:
    #         pass
            
            
            
            
    

    def text(self,player:'Player'):
        self_player:'Player'=player
        oppo_player:'Player'=player.opponent

        self_hand=','.join([card.text(player,False) for card in self_player.hand])
        oppo_hand=','.join([card.text(player,True) for card in oppo_player.hand])
        self_battle=','.join([card.text(player,False) for card in self_player.battlefield])
        oppo_battle=','.join([card.text(player,False) for card in oppo_player.battlefield])
        self_lands=','.join([card.text(player,False) for card in self_player.land_area])
        oppo_lands=','.join([card.text(player,False) for card in oppo_player.land_area])
        actions_text=','.join([action.text(player) for action in self.action_store_list if action.text(player) != ''])

        manas=[]
        for key in self_player.mana:
            if key!="colorless":
                manas.append(f'int({self_player.mana[key]})')
        manas=','.join(manas)
        time_turn=f'int({self.turn_timer})'
        time_bullet=f'int({self.bullet_timer})'
        life_self=f'int({self_player.life})'
        life_oppo=f'int({oppo_player.life})'
        len_deck_self=f'int({len(self_player.library)})'
        len_deck_oppo=f'int({len(oppo_player.library)})'
        your_turn=f'int({int(self_player==self.active_player)})'
        return f"Initinal_all(parameters({self_hand}),parameters({oppo_hand}),parameters({self_battle}),parameters({oppo_battle}),parameters({self_lands}),parameters({oppo_lands}),parameters({actions_text}),parameters({manas}),{time_turn},{time_bullet},{life_self},{life_oppo},{len_deck_self},{len_deck_oppo},{your_turn})"



    def __repr__(self):
        player1,player2=[key for key in self.players]
        if self.players[player1]==self.active_player:
            active_player_name=player1
            non_active_player_name=player2
        else:
            active_player_name=player2
            non_active_player_name=player1
        
        content=f"""


#########################################################################################
active_player:{active_player_name}
non_active_player:{non_active_player_name}

-----------------------------------------------------------------------------------
bullet_time:{str(self.get_flag("bullet_time"))}
attacter:{self.attacker}
-----------------------------------------------------------------------------------
player1:{player1}
    live:{self.players[player1].life}
    battle_field:{self.players[player1].battlefield}
    hand:{self.players[player1].hand}
    land:{self.players[player1].land_area}
    graveyard:{self.players[player1].graveyard}
    mana:{self.players[player1].mana}

player2:{player2}
    live:{self.players[player2].life}
    battle_field:{self.players[player2].battlefield}
    hand:{self.players[player2].hand}
    land:{self.players[player2].land_area}
    graveyard:{self.players[player2].graveyard}
    mana:{self.players[player2].mana}

Action_list:
    {self.action_store_list_cache}
#########################################################################################
        

"""
        return content
    
from game.buffs import StateBuff
async def tasks(room):
    await asyncio.sleep(6)
    for name in room.players:
        room.players[name].draw_card(2)
        print("draw cards")
        print(room.action_store_list_cache)
    #asyncio.create_task(room.message_receiver("t|play_card|1"))
async def main():
    test="Mistweaver Drake+Creature+1|Island+Land+4|Mystic Reflection+Instant+1|Mystic Evasion+Instant+2|Mindful Manipulation+Sorcery+1|Mistweaver Drake+Creature+1|Forest+Land+7|Aetheric Nexus+Land+1|Plains+Land+7|Swamp+Land+7|Mountain+Land+7|Mystic Tides+Instant+1"
    room=Room([(test,"CC"),(test,"DD")])
    
    await room.game_start()
    print([i.text(room.player_1) for i in room.player_1.hand])
    room.active_player=room.players["CC"]
    room.non_active_player=room.players["DD"]
    
    asyncio.create_task(room.message_receiver("CC|play_card|1"))
    await asyncio.sleep(6)
    print(room)
    print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
    
    asyncio.create_task(room.message_receiver("CC|play_card|1"))
    await asyncio.sleep(6)
    asyncio.create_task(room.message_receiver("CC|play_card|1"))
    
    await asyncio.sleep(6)
    asyncio.create_task(room.message_receiver("CC|activate_ability|land_area;0"))
    await asyncio.sleep(1)
    print(room)
    print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
    
    await asyncio.sleep(2)
    asyncio.create_task(room.message_receiver("CC|play_card|0"))
    await asyncio.sleep(6)
    print(room)
    print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
    
    await asyncio.sleep(2)
    asyncio.create_task(room.message_receiver("CC|end_step|"))
    await asyncio.sleep(2)
    asyncio.create_task(room.message_receiver("DD|play_card|1"))
    await asyncio.sleep(6)
    print(room)
    print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
    
    
    asyncio.create_task(room.message_receiver("DD|play_card|1"))
    await asyncio.sleep(6)
    asyncio.create_task(room.message_receiver("DD|play_card|1"))
    
    await asyncio.sleep(6)
    print(room)
    print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
    
    await asyncio.sleep(2)
    asyncio.create_task(room.message_receiver("DD|play_card|0"))
    await asyncio.sleep(6)
    print(room)
    print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
    
    await asyncio.sleep(2)
    
    await asyncio.sleep(5)
    card=room.active_player.battlefield[0]
    buff=StateBuff(card,2,2)
    card.gain_buff(buff)
    print(room)
    print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
    
    #card.loss_buff(buff)
    #print(room)

    await asyncio.sleep(2)
    asyncio.create_task(room.message_receiver("DD|select_attacker|0"))
    
    await asyncio.sleep(2)
    print(room)
    print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
    
    asyncio.create_task(room.message_receiver("CC|select_defender|0"))
    await asyncio.sleep(6)
    print(room)
    print('\n\n'.join([action.text(room.player_1) for action in room.action_store_list_cache]))
        
if __name__=="__main__":
    
        
    asyncio.run(main())
    
    

