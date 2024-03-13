from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.player import Player




from game.card import Card
from game.type_action import actions





class Creature(Card):

    def __init__(self) -> None:
        super().__init__()

        self.flag_dick:dict={}

        #the CreaturePara for js
        self.live:int
        self.power:int
        self.type_creature:str
    
    def grt_current_power_live(self)->tuple:# calculate power_live
        pass


    def check_dead(self):#check whether creature die
        pass

    #Here are listeners
    def when_enter_battlefield(self):# when creature enter battlefield
        pass

    def when_leave_battlefield(self):# when creature leave battlefield
        pass

    def when_die(self):
        pass

    def when_start_turn(self):
        pass

    def when_end_turn(self):
        pass

    def when_harm_is_done(self):#当造成伤害时
        pass

    def when_hurt(self):#当受到伤害时
        pass

    def when_being_treated(self):#当受到治疗时
        pass

    def when_become_attacker(self):
        pass

    def when_become_defender(self):
        pass

    def when_gain_buff(self):#当获得+1+1的buff时
        pass

    def when_loss_buff(self):#当失去+1+1的buff时
        pass

    def loss_buff(self,buff):
        pass

    def gain_buff(self,buff):
        pass

    def when_targeted(self):#When this creature is targeted
        pass

    # def when_play_this_card(self,player:'Player'=None,opponent:'Player'=None):# when player use the card
    #     pass

    def when_play_this_card(self, player: "Player" = None, opponent: "Player" = None):# when player use the card
        super().when_play_this_card(player, opponent)

        player.remove_card(self,"hand")
        player.append_card(self,"battlefield")
        # player.hand.remove(self)
        # player.battlefield.append(self)





