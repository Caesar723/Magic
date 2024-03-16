from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.player import Player



from game.game_function_tool import select_object
from game.card import Card
from game.type_action import actions





class Creature(Card):

    def __init__(self,player) -> None:
        super().__init__(player)

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
    
    #card1-start attack->card1-deal damage->card2-take_damage
    #card2-start defense->card2-deal damage->card1-take_damage
    # def start_attack(self,card:"Creature",player: "Player" = None, opponent: "Player" = None):#当两个creature 对战的时候,这个creature是attacter
    #     self.deal_damage(card,player,opponent)
        

    # def start_defense(self,card:"Creature",player: "Player" = None, opponent: "Player" = None):#当两个creature 对战的时候,这个creature是defender
    #     self.deal_damage(card,player,opponent)

    def deal_damage(self,card:"Creature",player: "Player" = None, opponent: "Player" = None):# 用在所有造成伤害的功能
        power,life=self.state
        
        card.take_damage(self,power,card.player,card.player.opponent) 
        self.when_harm_is_done(card,power,player,opponent)
        

        

    def take_damage(self,card:Card,value:int,player: "Player" = None, opponent: "Player" = None)->int:# 可以受到来自各种卡牌的伤害
        print(value,card)
        self.actual_live-=value
        self.when_hurt(card,value,player,opponent)
        return value

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

    def when_harm_is_done(self,card:"Creature",value:int,player: "Player" = None, opponent: "Player" = None):#当造成伤害时
        return value

    def when_hurt(self,card:"Creature",value:int,player: "Player" = None, opponent: "Player" = None):#当受到伤害时
        return value

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

    def when_kill_creature(self,card:"Creature",player: "Player" = None, opponent: "Player" = None):
        pass

    def when_start_attcak(self,card:"Creature",player: "Player" = None, opponent: "Player" = None):
        pass

    def when_start_defend(self,card:"Creature",player: "Player" = None, opponent: "Player" = None):
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
        power,live=self.state
        content=f"({self.name},{self.type},{power}/{live},{id(self)})"
        return content





