
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

        self.mana_cost:str="2W"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Destroy target land. Its controller gains 3 life."
        self.image_path:str="cards/sorcery/Divine Offering/image.jpg"

    @select_object("opponent_lands",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if selected_object:
            target=selected_object[0]
            if target in opponent.land_area:
                await self.destroy_land(target, "rgba(255,0,0,0.5)", "Missile_Hit")
            await self.cure_to_object(opponent, 3, "rgba(0,255,0,1)", "Cure")




        