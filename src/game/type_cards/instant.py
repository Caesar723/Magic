from typing import TYPE_CHECKING,Union
import json

#from game.player import Player
if TYPE_CHECKING:
    from game.player import Player
    from game.type_cards.creature import Creature





from game.card import Card
from game.type_action import actions
from game.game_function_tool import select_object



class Instant(Card):
    
    def __init__(self,player) -> None:
        super().__init__(player)

    @select_object("",1)
    async def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        pass

    def calculate_spell_power(self):
        pass

    def when_select_target(self):
        pass

    async def when_play_this_card(self,player:'Player'=None,opponent:'Player'=None):# when player use the card
        await super().when_play_this_card(player, opponent)

       

        prepared_function=await self.card_ability(player,opponent)
        if prepared_function=="cancel":
            return prepared_function

        player.remove_card(self,"hand")
        player.append_card(self,"graveyard")
        
        return prepared_function
    
    async def attact_to_object(self,object:Union["Creature","Player"],power:int,color:str,type_missile:str):# it won't get hurt object can be card ot player
        if isinstance(object,(type(self.player),type(self.player.opponent))):
            object.take_damage(self,power)
            self.player.action_store.add_action(actions.Attack_To_Object(self.player,self.player,object,color,type_missile,[object.life]))
            await object.check_dead()
        else:
            object.take_damage(self,power,object.player,object.player.opponent) 
            self.player.action_store.add_action(actions.Attack_To_Object(self.player,self.player,object,color,type_missile,object.state))
            if await object.check_dead():
                self.when_kill_creature(object,self.player,self.player.opponent)
    
    
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
        buffs=f"parameters({','.join([buff.text(player) for buff in self.buffs])})"
        return f"Instant({Flag_dict},{Counter_dict},{Player},int({Id}),string({Name}),{Type},{Type_card},{Rarity},string({Content}),string({Image_Path}),{Fee},{buffs})"

    def __repr__(self):
        content=f"({self.name},{self.type},{id(self)},{self.mana_cost})"
        return content
    
class Instant_Undo(Instant):
    def __init__(self,player:"Player") -> None:
        super().__init__(player)
        self.undo_range="all"#all,Sorcery|Creature|Instant|Land这个是是all 或者是 Sorcery|Creature这样的组合
        self.stack=player.room.stack
        self.get_flag_room=player.room.get_flag

    def check_can_use(self, player: 'Player') -> tuple[bool]:
        result= super().check_can_use(player)
        if not self.get_flag_room("bullet_time"):
            return [False,"You can't use this card out of bullet time"]
        
        
        if self.undo_range=="all" and self.stack:
            func,card=self.stack[-1]
            if card.type=="Creature" and self.get_flag_room("attacker_defenders"):
                return [False,"You can't use this card on a defense creature"]
            elif card.type!="Land":
                return result
            else:
                return [False,"You can't use this card on a land"]
        elif self.stack:
            func,card=self.stack[-1]
            ranges=self.undo_range.split("|")
            if card.type in ranges:
                if card.type=="Creature" and self.get_flag_room("attacker_defenders"):
                    return [False,"You can't use this card on a defense creature"]
                return result
            else:
                return [False,"You can't use this card"]
        else:
            return [False,"You can't use this card"]
        
    

    async def undo_stack(self,player:'Player'=None,opponent:'Player'=None)->tuple[callable,Card]:
        
        func,card=self.stack.pop()
        if card.type=="Creature" :
            if card in opponent.battlefield:
                opponent.remove_card(card,"battlefield")
                opponent.append_card(card,"graveyard")
            else:
                player.remove_card(card,"battlefield")
                player.append_card(card,"graveyard")
        return func,card

        
        
    @select_object("",1)
    async def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        pass