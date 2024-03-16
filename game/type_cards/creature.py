from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.player import Player



from game.game_function_tool import select_object
from game.card import Card
from game.type_action import actions





class Creature(Card):

    def __init__(self) -> None:
        super().__init__()

        self.flag_dick:dict={}

        #the CreaturePara for js
        
        self.live:int
        self.power:int

        self.actual_live:int
        self.actual_power:int
        
        self.type_creature:str
    
    @property
    def state(self):
        return (self.actual_power,self.actual_live)
    
    def take_damage_attack(self,card:"Creature"):#当两个creature 对战的时候
        pass

    def take_damage(self,damage:int):# 用在所有受伤的功能
        pass

    def grt_current_power_live(self)->tuple:# calculate power_live
        pass


    def check_dead(self):#check whether creature die,or whether appear at battle field
        pass

    #Here are listeners
    @select_object("",1)
    def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None,selected_object:tuple['Card']=()):# when creature enter battlefield
        pass

    def when_leave_battlefield(self,player: "Player" = None, opponent: "Player" = None):# when creature leave battlefield
        pass

    def when_die(self,player: "Player" = None, opponent: "Player" = None):
        pass

    def when_start_turn(self,player: "Player" = None, opponent: "Player" = None):
        pass

    def when_end_turn(self,player: "Player" = None, opponent: "Player" = None):
        pass

    def when_harm_is_done(self,player: "Player" = None, opponent: "Player" = None):#当造成伤害时
        pass

    def when_hurt(self,player: "Player" = None, opponent: "Player" = None):#当受到伤害时
        pass

    def when_being_treated(self,player: "Player" = None, opponent: "Player" = None):#当受到治疗时
        pass

    def when_become_attacker(self,player: "Player" = None, opponent: "Player" = None):
        pass

    def when_become_defender(self,player: "Player" = None, opponent: "Player" = None):
        pass

    def when_gain_buff(self,player: "Player" = None, opponent: "Player" = None):#当获得+1+1的buff时
        pass

    def when_loss_buff(self,player: "Player" = None, opponent: "Player" = None):#当失去+1+1的buff时
        pass

    def loss_buff(self,buff):
        pass

    def gain_buff(self,buff):
        pass

    def when_targeted(self):#When this creature is targeted
        pass

    # def when_play_this_card(self,player:'Player'=None,opponent:'Player'=None):# when player use the card
    #     pass
    
    

    async def when_play_this_card(self, player: "Player" = None, opponent: "Player" = None):# when player use the card
        await super().when_play_this_card(player, opponent)

        player.remove_card(self,"hand")
        player.append_card(self,"battlefield")
        prepared_function=await self.when_enter_battlefield(player,opponent)
        print(1)
        return prepared_function
        # player.hand.remove(self)
        # player.battlefield.append(self)
    
    def __repr__(self):
        content=f"({self.name},{self.type},{self.live}/{self.power},{id(self)})"
        return content





