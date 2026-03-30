
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Celestial_Purge(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=192

        self.name:str="Celestial Purge"

        self.type:str="Sorcery"

        self.mana_cost:str="2W"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Exile target black or red permanent."
        self.image_path:str="cards/sorcery/Celestial Purge/image.jpg"

    @select_object("opponent_roles",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if selected_object:
            target = selected_object[0]
            if hasattr(target, 'color') and target.color in ['black', 'red']:
                await self.exile_object(target, "rgba(239, 228, 83, 0.8)", "Missile_Hit")




        