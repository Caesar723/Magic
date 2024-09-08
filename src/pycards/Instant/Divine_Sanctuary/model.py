
from __future__ import annotations
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from game.buffs import Buff
from game.type_cards.creature import Creature

class Divine_Sanctuary_Buff(Buff):
    def __init__(self,card:"Card",selected_card:"Card") -> None:
        super().__init__(card,selected_card)
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str="immunity"#这个buff是用在那个类型的
        self.name="Divine Sanctuary"
        self.content="immunity"
        self.color_missile="rgba(255, 215, 0, 0.9)"

    def change_function(self,card:"Creature"):
        previews_func_flag=card.get_flag
        previews_func_take_damage=card.take_damage

        async def take_damage(self_card,card,value,player, opponent):# 可以受到来自各种卡牌的伤害
            result=await previews_func_take_damage(card,0,player,opponent)
            return result

        def get_flag(self_card,key):
            result=previews_func_flag(key)
            if key=="die":
                return False
            return result
        
        def die(self_card):
            pass

        def gain_buff(self_card:Creature,buff:Buff,card):
            pass

        card.get_flag = types.MethodType(get_flag, card)
        card.die = types.MethodType(die, card)
        card.gain_buff = types.MethodType(gain_buff, card)
        card.take_damage = types.MethodType(take_damage, card)

class Divine_Sanctuary(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Divine Sanctuary"

        self.type:str="Instant"

        self.mana_cost:str="4WW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Until the end of your turn, you and all creatures you control gain immunity to all effects."
        self.image_path:str="cards/Instant/Divine Sanctuary/image.jpg"


    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        for creature in player.battlefield:
            buff=Divine_Sanctuary_Buff(self,creature)
            buff.set_end_of_turn()
            creature.gain_buff(buff,self)



        