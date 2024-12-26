import time

from game.agent import Agent_Player_Red as Agent
from game.player_agent_room import PVE_Room
from game.studio_class import generate_creature_class,generate_instant_class,generate_land_class,generate_sorcery_class
from game.player import Player
from game.card import Card
from server_function_tool import Studio_Card_Data
from initinal_file import CARD_DICTION

class Studio_Player(Player):
    def __init__(self,name:str,room:"Studio_Room") -> None:
        super().__init__(name,"",room)

    def draw_card(self,number:int):# draw x cards from library
        self.action_store.start_record()
        for i in range(number):
            if not (self.library):
                #self.flag_dict["die"]=True
                self.action_store.end_record()
                return 
            card=self.library[0]
            self.remove_card(card,'library')
            self.append_card(card,'hand')
        self.action_store.end_record()

    def initinal_decks(self,decks_detail:str):#generate cards
        # print(decks_detail)
        # print(decks_detail.split("|"))
        # for element in decks_detail.split("|"):
        #     name,type,number=element.split("+")
        #     number=int(number)
        #     self.deck+=[CARD_DICTION[f"{name}_{type}"](self) for i in range(number)]
        # random.shuffle(self.deck)
        # self.hand=self.deck[:7]# get 7 card to hand
        # self.library=self.deck[7:]# the rest is in the library
        pass

class Studio_Room(PVE_Room):
    def __init__(self,players:list[tuple],room_server) -> None:
        super().__init__(players,room_server)

        self.message_process_dict["add_card"]=self.add_card

    def initinal_player(self,players:list[tuple]):
        #agents_deck="Eternal Phoenix+Creature+4|Raging Firekin+Creature+4|Emberheart Salamander+Creature+4|Arcane Inferno+Instant+4|Pyroblast Surge+Instant+4|Fiery Blast+Instant+4|Inferno Titan+Creature+4|Flame Tinkerer+Creature+4|Mountain+Land+24"

        # Agent_para=[(agents_deck,"Agent1")]
        print(self.stack)
        self.player_1,self.player_2=Agent("Agent1",self),\
                                    Studio_Player(players[0][1],self)
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

    async def add_card(self,username:str,content:str):
        """
        ...|add_card|name+type+number
        """
        name,type,number=content.split("+")
        number=int(number)
        self.action_processor.start_record()
        for i in range(number):
            if f"{name}_{type}" in CARD_DICTION:
                card=CARD_DICTION[f"{name}_{type}"](self.players[username])
                self.players[username].append_card(card,'hand')
            else:
                print(f"{name}_{type} not found")
        self.action_processor.end_record()

    async def update_timer(self):# update turn_timer and bullet_time_timer
        if self.get_flag("bullet_time"):
            self.bullet_timer:int=self.max_bullet_time-round(time.perf_counter()-self.initinal_bullet_timer)
            await self.check_timer_change("timer_bullet",self.bullet_timer)
            #print(self.bullet_timer)
            if self.bullet_timer<=0:
                await self.end_bullet_time()
        else:
            #self.initinal_turn_timer-=round(time.perf_counter()-self.initinal_turn_timer)
            #self.turn_timer:int=self.max_turn_time-round(time.perf_counter()-self.initinal_turn_timer)
            self.turn_timer=self.max_turn_time
            await self.check_timer_change("timer_turn",self.turn_timer)
            if self.turn_timer<=0:
                await self.end_turn_time()

    def add_studio_card(self,datas:Studio_Card_Data,name:str):
       print(datas)
       print(dict(datas))
       player=self.players[name]
       dict_function={
           "Creature":generate_creature_class,
           "Instant":generate_instant_class,
           "Land":generate_land_class,
           "Sorcery":generate_sorcery_class
       }
       #for data in datas:
       card_class=dict_function[datas.init_type](**(datas.dict()))
       print(card_class)
       card=card_class(player)

       self.action_processor.start_record()
       player.append_card(card,'hand')
       self.action_processor.end_record()

       pass

    async def update_task(self,died_player:list[Player]):
        pass
