from typing import TYPE_CHECKING,Union
import json
if TYPE_CHECKING:
    from game.player import Player
    from game.type_cards.creature import Creature





from game.card import Card
from game.type_action import actions
from game.game_function_tool import select_object


class Sorcery(Card):
    
    def __init__(self,player) -> None:
        super().__init__(player)

    @select_object("",1)
    async def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):# when player use the card
        pass

    def calculate_spell_power(self):
        pass

    def when_select_target(self):
        pass

    async def when_play_this_card(self,
                            player:'Player'=None,
                            opponent:'Player'=None,
                            ):# when player use the card
        await super().when_play_this_card(player, opponent)

        
        prepared_function=await self.card_ability(player,opponent)
        if prepared_function=="cancel":
            return prepared_function
        player.remove_card(self,"hand")
        player.append_card(self,"graveyard")
        return prepared_function
    
    async def attact_to_object(self,object:Union["Creature","Player"],power:int,color:str,type_missile:str):# it won't get hurt object can be card ot player
        if isinstance(object,(type(self.player),type(self.player.opponent))):
            await object.take_damage(self,power)
            self.player.action_store.add_action(actions.Attack_To_Object(self.player,self.player,object,color,type_missile,[object.life]))
            await object.check_dead()
        else:
            await object.take_damage(self,power,object.player,object.player.opponent) 
            self.player.action_store.add_action(actions.Attack_To_Object(self.player,self.player,object,color,type_missile,object.state))
            if await object.check_dead():
                await self.when_kill_creature(object,self.player,self.player.opponent)
    
    async def cure_to_object(self,object:Union["Creature","Player"],power:int,color:str,type_missile:str):# it won't get hurt
        if isinstance(object,(type(self.player),type(self.player.opponent))):
            await object.gains_life(self,power)
            self.player.action_store.add_action(actions.Cure_To_Object(self.player,self.player,object,color,type_missile,[object.life]))
            await object.check_dead()
        else:
            await object.gains_life(self,power,object.player,object.player.opponent) 
            self.player.action_store.add_action(actions.Cure_To_Object(self.player,self.player,object,color,type_missile,object.state))
            if await object.check_dead():
               await self.when_kill_creature(object,self.player,self.player.opponent)
    
    async def destroy_object(self,object:"Creature",color:str,type_missile:str):
        object.flag_dict["die"]=True
        self.player.action_store.add_action(actions.Attack_To_Object(self.player,self.player,object,color,type_missile,object.state))
        if await object.check_dead():
            await self.when_kill_creature(object,self.player,self.player.opponent)
            
    async def exile_object(self,object:"Creature",color:str,type_missile:str):
        object.flag_dict["exile"]=True
        self.player.action_store.add_action(actions.Attack_To_Object(self.player,self.player,object,color,type_missile,object.state))
     
    
    def text(self,player:'Player',show_hide:bool=False)-> str:
        
        Flag_dict=f"str2json(string({json.dumps(self.flag_dict)}))"
        Counter_dict=f"str2json(string({json.dumps(self.counter_dict)}))"
        Player=self.player.text(player)
        Id=id(self)
        if show_hide and player.name!=self.player.name:
            return f"Opponent({Player},int({Id}))"
        Name=self.name
        Type=self.color
        Type_card=self.type_card
        Rarity=self.rarity
        Content=self.content
        Image_Path=self.image_path
        Fee=self.mana_cost
        buffs=f"parameters({','.join([buff.text(player) for buff in self.buffs])})"
        return f"Sorcery({Flag_dict},{Counter_dict},{Player},int({Id}),string({Name}),{Type},{Type_card},{Rarity},string({Content}),string({Image_Path}),{Fee},{buffs})"

    
    def __repr__(self):
        content=f"({self.name},{self.type},{id(self)},{self.mana_cost})"
        return content