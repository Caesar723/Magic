from typing import TYPE_CHECKING,Union
import json
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
        
        rest_live=card.take_damage(self,power,card.player,card.player.opponent) 
        await self.when_harm_is_done(card,power,player,opponent)
        if await card.check_dead():
            self.when_kill_creature(card,player,opponent)
        return rest_live
        
            #self.player.action_store.add_action(actions.Attack_To_Object(self,self.player,opponent,"rgba(243, 243, 243, 0.9)","Missile_Hit",(opponent.life)))


    async def deal_damage_player(self,player:"Player",player_attacker: "Player" = None, opponent_attacker: "Player" = None):
        power,life=self.state
        player.take_damage(self,power)
        await self.when_harm_is_done(player,power,player_attacker,opponent_attacker)
        await player.check_dead()
            


        
    def gains_life(self,card:Card,value:int,player: "Player" = None, opponent: "Player" = None):
        self.actual_live+=value
        if self.actual_live>self.live:
            self.actual_live=self.live
        self.when_being_treated(card,value,player,opponent)
        return self.state[1]
    
    def take_damage(self,card:Card,value:int,player: "Player" = None, opponent: "Player" = None)->int:# 可以受到来自各种卡牌的伤害
        #print(value,card)
        self.actual_live-=value
        self.when_hurt(card,value,player,opponent)
        return self.state[1]

    # def grt_current_power_live(self)->tuple:# calculate power_live
    #     pass

    # async def attact_to_object(self,object:Union["Creature","Player"],power:int,color:str,type_missile:str):# it won't get hurt object can be card ot player
    #     await super().attact_to_object(object,power,color,type_missile)
    #     await self.when_harm_is_done(object,power,self.player,self.player.opponent)
    

    #Here are listeners 注意，这个是异步函数
    @select_object("",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None,selected_object:tuple['Card']=()):# when creature enter battlefield . selection_random=true when user not select it will select random
        pass#这个是玩家打出牌的时候

    def when_go_to_battlefield(self, player: "Player" = None, opponent: "Player" = None):#这个是每次进入场地的时候
        self.flag_dict["summoning_sickness"]=True
    def end_summoning_sickness(self):
        self.flag_dict["summoning_sickness"]=False

    def when_leave_battlefield(self,player: "Player" = None, opponent: "Player" = None,name:str='battlefield'):# when creature leave battlefield
        player.remove_card(self,"battlefield")
        player.append_card(self,name)

    async def when_die(self,player: "Player" = None, opponent: "Player" = None):#OK
        pass

    def when_start_turn(self,player: "Player" = None, opponent: "Player" = None):#OK
        pass

    def when_end_turn(self,player: "Player" = None, opponent: "Player" = None):#OK
        pass

    async def when_harm_is_done(self,card:Union["Creature","Player"],value:int,player: "Player" = None, opponent: "Player" = None):#当造成伤害时 OK
        return await super().when_harm_is_done(card,value,player,opponent)

    def when_hurt(self,card:"Creature",value:int,player: "Player" = None, opponent: "Player" = None):#当受到伤害时 OK
        return value

    def when_being_treated(self,card:"Creature",player: "Player" = None, opponent: "Player" = None):#当受到治疗时
        pass

    def when_become_attacker(self,player: "Player" = None, opponent: "Player" = None):# OK
        pass

    def when_become_defender(self,player: "Player" = None, opponent: "Player" = None):# OK
        pass

    

    def when_kill_creature(self,card:"Creature",player: "Player" = None, opponent: "Player" = None):#OK
        pass

    def when_start_attcak(self,card:Union["Creature","Player"],player: "Player" = None, opponent: "Player" = None):#OK
        pass

    def when_start_defend(self,card:"Creature",player: "Player" = None, opponent: "Player" = None):#OK
        pass

    
    

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
        await self.when_die(player,opponent)
        self.when_leave_battlefield(player,opponent,'graveyard')
        self.reset_to_orginal_state()
        
        # player.remove_card(self,"battlefield")
        # player.append_card(self,"graveyard")
    
    async def when_move_to_exile_area(self, player: "Player" = None, opponent: "Player" = None):
        self.when_leave_battlefield(player,opponent,'exile_area')
        self.reset_to_orginal_state()
    

    async def when_play_this_card(self, player: "Player" = None, opponent: "Player" = None):# when player use the card OK
        await super().when_play_this_card(player, opponent)

        


        prepared_function=await self.when_enter_battlefield(player,opponent)
        if prepared_function=="cancel":
            return prepared_function

        player.remove_card(self,"hand")
        player.append_card(self,"battlefield")

        #print("battlefield")
        return prepared_function
        # player.hand.remove(self)
        # player.battlefield.append(self)

    async def when_clicked(self):
        pass

    def tap(self):
        if not self.get_flag("tap"):
            self.player.action_store.add_action(actions.Activate_Ability(self,self.player))
            self.flag_dict["tap"]=True#横置

    def untap(self):
        if self.get_flag("tap"):
            self.player.action_store.add_action(actions.Reset_Ability(self,self.player))
            self.flag_dict["tap"]=False#横置
    
    def reset_to_orginal_state(self):
        self.actual_live=self.live
        self.actual_power=self.power
        reset_instance_methods(self)

    def when_gain_buff(self,player: "Player" = None, opponent: "Player" = None,buff:Buff=None,card:'Card'=None):#当获得+1+1的buff时 OK
        self.player.action_store.start_record()
        
    
        
        self.player.action_store.add_action(actions.Add_Buff(card,self.player,self,"rgba(236, 230, 233, 0.8)","Missile_Hit",self.state,buff,True))
        self.player.action_store.end_record()

    def when_loss_buff(self,player: "Player" = None, opponent: "Player" = None,buff:Buff=None,card:'Card'=None):#当失去+1+1的buff时 OK
        self.player.action_store.start_record()

        self.player.action_store.add_action(actions.Lose_Buff(card,self.player,self,self.state,buff,True))
        self.player.action_store.end_record()


    def text(self,player:'Player',show_hide:bool=False)-> str:
        
        Flag_dict=f"str2json(string({json.dumps(self.flag_dict)}))"
        Counter_dict=f"str2json(string({json.dumps(self.counter_dict)}))"
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

        state=self.state
        Org_Life=self.live
        Life=state[1]
        Org_Damage=self.power
        Damage=state[0]
        
        buffs=f"parameters({','.join([buff.text(player) for buff in self.buffs])})"
        return f"Creature({Flag_dict},{Counter_dict},{Player},int({Id}),string({Name}),{Type},{Type_card},{Rarity},string({Content}),string({Image_Path}),{Fee},int({Org_Life}),int({Life}),int({Org_Damage}),int({Damage}),{buffs})"



    
    
    def __repr__(self):
        power,live=self.state
        
        content=f"({self.name},{self.type},{power}/{live},{id(self)},{self.mana_cost})"
        return content





