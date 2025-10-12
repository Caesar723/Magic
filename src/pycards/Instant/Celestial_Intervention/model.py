
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from game.buffs import Indestructible

class Celestial_Intervention(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Celestial Intervention"

        self.type:str="Instant"

        self.mana_cost:str="2WW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Until end of turn, creatures you control gain indestructible. You draw a card."
        self.image_path:str="cards/Instant/Celestial Intervention/image.jpg"


    @select_object("",1)
    async def card_ability(self,player:Player,opponent:Player,selected_object:tuple[Card]):
        for creature in player.battlefield:
            buff=Indestructible(self,creature)
            buff.set_end_of_turn()
            creature.gain_buff(buff,self)
        player.draw_card(1)

        