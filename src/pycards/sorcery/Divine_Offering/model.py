
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Divine_Offering(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=200

        self.name:str="Divine Offering"

        self.type:str="Sorcery"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Destroy target artifact. Its controller gains 3 life."
        self.image_path:str="cards/sorcery/Divine Offering/image.jpg"

    @select_object("opponent_permanents",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if selected_object:
            await self.destroy_object(selected_object[0], "rgba(255,0,0,0.5)", "Missile_Hit")
            await opponent.gains_life(self,3)




        