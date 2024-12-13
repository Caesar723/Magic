

from game.agent import Agent_Player_Red as Agent
from game.player_agent_room import PVE_Room
from game.player import Player
from game.card import Card
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
        for i in range(number):
            if f"{name}_{type}" in CARD_DICTION:
                card=CARD_DICTION[f"{name}_{type}"](self.players[username])
                self.players[username].append_card(card,'hand')
            else:
                print(f"{name}_{type} not found")

    