from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.player import Player



from game.game_function_tool import select_object,backup_instance_methods,reset_instance_methods
from game.card import Card
from game.type_action import actions
from game.buffs import Buff




class Creature(Card):

    def __init__(self,player) -> None:
        super().__init__(player)

        self.flag_dict:dict={}
        self.buffs:list[Buff]=[]

        #the CreaturePara for js
        
        self.live:int
        self.power:int

        self.actual_live:int
        self.actual_power:int
        
        self.type_creature:str

        backup_instance_methods(self)#用在buff的，因为buff会改变函数，所以需要重置函数
    
    @property
    def state(self):
        state=self.calculate_state()
        return state
    
    def calculate_state(self):
        return (self.actual_power,self.actual_live)
    
    def get_flag(self,flag_name:str):
        if flag_name in self.flag_dict:
            return self.flag_dict[flag_name]
        else:
            return False
    #card1-start attack->card1-deal damage->card2-take_damage
    #card2-start defense->card2-deal damage->card1-take_damage
    # def start_attack(self,card:"Creature",player: "Player" = None, opponent: "Player" = None):#当两个creature 对战的时候,这个creature是attacter
    #     self.deal_damage(card,player,opponent)
        

    # def start_defense(self,card:"Creature",player: "Player" = None, opponent: "Player" = None):#当两个creature 对战的时候,这个creature是defender
    #     self.deal_damage(card,player,opponent)

    async def deal_damage(self,card:"Creature",player: "Player" = None, opponent: "Player" = None):# 用在所有造成伤害的功能
        power,life=self.state
        
        card.take_damage(self,power,card.player,card.player.opponent) 
        self.when_harm_is_done(card,power,player,opponent)
        if await card.check_dead():
            self.when_kill_creature(card,player,opponent)
        

        

    def take_damage(self,card:Card,value:int,player: "Player" = None, opponent: "Player" = None)->int:# 可以受到来自各种卡牌的伤害
        print(value,card)
        self.actual_live-=value
        self.when_hurt(card,value,player,opponent)
        return value

    # def grt_current_power_live(self)->tuple:# calculate power_live
    #     pass


    

    #Here are listeners
    @select_object("",1)
    def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None,selected_object:tuple['Card']=()):# when creature enter battlefield
        pass

    def when_leave_battlefield(self,player: "Player" = None, opponent: "Player" = None,name:str='battlefield'):# when creature leave battlefield
        player.remove_card(self,"battlefield")
        player.append_card(self,name)

    def when_die(self,player: "Player" = None, opponent: "Player" = None):#OK
        pass

    def when_start_turn(self,player: "Player" = None, opponent: "Player" = None):#OK
        pass

    def when_end_turn(self,player: "Player" = None, opponent: "Player" = None):#OK
        pass

    def when_harm_is_done(self,card:"Creature",value:int,player: "Player" = None, opponent: "Player" = None):#当造成伤害时 OK
        return value

    def when_hurt(self,card:"Creature",value:int,player: "Player" = None, opponent: "Player" = None):#当受到伤害时 OK
        return value

    def when_being_treated(self,player: "Player" = None, opponent: "Player" = None):#当受到治疗时
        pass

    def when_become_attacker(self,player: "Player" = None, opponent: "Player" = None):# OK
        pass

    def when_become_defender(self,player: "Player" = None, opponent: "Player" = None):# OK
        pass

    def when_gain_buff(self,player: "Player" = None, opponent: "Player" = None):#当获得+1+1的buff时 OK
        pass

    def when_loss_buff(self,player: "Player" = None, opponent: "Player" = None):#当失去+1+1的buff时 OK
        pass

    def when_kill_creature(self,card:"Creature",player: "Player" = None, opponent: "Player" = None):#OK
        pass

    def when_start_attcak(self,card:"Creature",player: "Player" = None, opponent: "Player" = None):#OK
        pass

    def when_start_defend(self,card:"Creature",player: "Player" = None, opponent: "Player" = None):#OK
        pass

    def loss_buff(self,buff):
        if buff in self.buffs:
            self.buffs.remove(buff)
            self.update_buff()
            self.when_loss_buff(self.player,self.player.opponent)
        else:
            self.update_buff()
        

    def gain_buff(self,buff):
        self.buffs.append(buff)
        self.update_buff()
        self.when_gain_buff(self.player,self.player.opponent)

    def update_buff(self):
        reset_instance_methods(self)
        self.change_function_by_buff()
        
    def change_function_by_buff(self):#遍历buffs，改变函数
        for buff in self.buffs:
            buff.change_function(self)

    def when_targeted(self):#When this creature is targeted
        pass

    # def when_play_this_card(self,player:'Player'=None,opponent:'Player'=None):# when player use the card
    #     pass
    async def check_dead(self):#check whether creature die,or whether appear at battle field
        power,live=self.state
        if live<=0:
            self.flag_dict["die"]=True
            return True
        else:
            return False
        
    async def when_move_to_graveyard(self, player: "Player" = None, opponent: "Player" = None):#移入墓地 OK
        self.when_die(player,opponent)
        self.when_leave_battlefield(player,opponent,'graveyard')
        self.reset_to_orginal_state()
        
        # player.remove_card(self,"battlefield")
        # player.append_card(self,"graveyard")
    
    

    async def when_play_this_card(self, player: "Player" = None, opponent: "Player" = None):# when player use the card OK
        await super().when_play_this_card(player, opponent)

        player.remove_card(self,"hand")
        player.append_card(self,"battlefield")


        prepared_function=await self.when_enter_battlefield(player,opponent)

        print("battlefield")
        return prepared_function
        # player.hand.remove(self)
        # player.battlefield.append(self)

    async def when_clicked(self):
        pass

    
    
    def reset_to_orginal_state(self):
        self.actual_live=self.live
        self.actual_power=self.power
        reset_instance_methods(self)

    def text(self,player:'Player',show_hide:bool=False)-> str:
        Flying=int(self.get_flag("flying"))
        Active=int(self.get_flag("active"))
        Player=self.player.text(player)
        Id=id(self)
        Name=self.name
        if show_hide and player.name!=self.player.name:
            return f"Opponent({Player},int({Id}))"
        Type=self.color
        Type_card=self.type_card
        Rarity=self.rarity
        Content=self.content
        Image_Path=self.image_path
        Fee=self.mana_cost
        Org_Life=self.live
        Life=self.actual_live
        Org_Damage=self.power
        Damage=self.actual_power
        return f"Creature({Flying},{Active},{Player},int({Id}),string({Name}),{Type},{Type_card},{Rarity},string({Content}),{Image_Path},{Fee},int({Org_Life}),int({Life}),int({Org_Damage}),int({Damage}))"



    
    
    def __repr__(self):
        power,live=self.state
        flying=self.get_flag("flying")
        active=self.get_flag("active")
        content=f"({self.name},{self.type},{power}/{live},{id(self)},{self.mana_cost})"
        return content





