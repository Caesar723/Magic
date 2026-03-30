
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Flames_of_Fury(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=209

        self.name:str="Flames of Fury"

        self.type:str="Sorcery"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Flames of Fury deals 3 damage to target creature or player. If you control a Mountain, Flames of Fury deals 1 additional damage."
        self.image_path:str="cards/sorcery/Flames of Fury/image.jpg"

    @select_object("all_roles",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if not selected_object:
            return
        has_mountain = any(getattr(land, "name", "") == "Mountain" for land in player.land_area)
        damage = 4 if has_mountain else 3
        await self.attact_to_object(selected_object[0], damage, "rgba(255,0,0,1)", "Missile_Hit")


        