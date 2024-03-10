



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
        self.players:dict={
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

