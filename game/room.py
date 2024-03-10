



from game.player import Player
from game.action import Action
from game.card import Card





class Room:
    
    
    def __init__(self,players:list[tuple]) -> None:#((deck,user_name1),...)
        #used to store all action
        self.action_store_list:list[Action]=[]

        #used to count the time for a turn
        self.turn_timer:int=0
        self.max_turn_time:int=60

        #used to count the time when player use instant and in bullet_time
        self.bullet_timer:int=0
        self.max_bullet_time:int=5

        # used to store the players
        player_1,player_2=Player(players[0][1],players[0][0]),Player(players[1][1],players[1][0])
        player_1.set_opponent_player(player_2)
        player_2.set_opponent_player(player_1)
        self.players:dict={
            players[0][1]:player_1,
            players[1][1]:player_2
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
        self.stack:list[tuple]=[]#(preparend_function,card)

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

        }

    

    def start_attack(self):# attacker and defenders start attack
        pass

    def update_timer(self):# update turn_timer and bullet_time_timer
        pass
        

    def end_turn_time(self):#turn_timer is 0
        pass

    def end_bullet_time(self):#bullet_time is 0
        pass

    def reset_turn_timer(self):
        pass

    def reset_bullet_timer(self):
        pass

    def change_turn(self):# when active_player end turn
        pass

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
        
        """
        username,type,content=message.split("|")
        if type in self.message_process_dict:
            self.message_process_dict[type](username,content)

        
    
    def select_attacker(self,username:str,content:str):
        player:Player=self.players[username]
        if player==self.active_player:
            player.select_attacker(int(content))
            return (True,"success")
        else:
            return (False,"You must attack in your turn")

    def select_defender(self,username:str,content:str):
        pass

    def play_card(self,username:str,content:str):
        player:Player=self.players[username]
        index=int(content)
        if player==self.active_player:
            card=player.get_card_index(index,"hand")
            player.play_a_card(card)
            return (True,"success")
        else:
            return (False,"You must attack in your turn")

    def end_step(self,username:str,content:str):
        pass

    def discard(self,username:str,content:str):
        pass

    def activate_ability(self,username:str,content:str):
        pass

    def concede(self,username:str,content:str):
        pass

    def set_socket(self,socket,username:str):#用来初始化socket
        self.players_socket[username]=socket

