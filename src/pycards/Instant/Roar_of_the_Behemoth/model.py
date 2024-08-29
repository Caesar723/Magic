
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


class Roar_of_the_Behemoth_Buff(Buff):
    def __init__(self,card:"Card",selected_card:"Card") -> None:
        super().__init__(card,selected_card)
        self.buff_name=f"{card.name}"
        self.content="0 power until the end of this turn."
        self.color_missile="rgba(203, 203, 203, 0.9)"
        self.buff_missile="Missile_Hit"
        self.card_type:str="State"#这个buff是用在那个类型的

    def change_function(self,card:"Creature"):
        previews_func=card.calculate_state
        def calculate_state(self_card):
            power,live=previews_func()
            power=0
            return (power,live)
        card.calculate_state = types.MethodType(calculate_state, card)

    def set_end_of_turn(self):
        self.card.player.put_card_to_dict("end_step_buff",self)

    def when_end_turn(self):
        self.selected_card.loss_buff(self,self.card)
        self.card.player.remove_card_from_dict("end_step_buff",self)



class Roar_of_the_Behemoth(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Roar of the Behemoth"

        self.type:str="Instant"

        self.mana_cost:str="3GG"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="All enemy creatures get 0 power until the end of this turn."
        self.image_path:str="cards/Instant/Roar of the Behemoth/image.jpg"


    @select_object("",1)
    async def card_ability(self,player:Player,opponent:Player,selected_object:tuple["Card"]):
        for creature_opponent in opponent.battlefield:
            buff=Roar_of_the_Behemoth_Buff(self,creature_opponent)
            buff.set_end_of_turn()
            creature_opponent.gain_buff(buff,self)