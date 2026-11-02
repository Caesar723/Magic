from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Hollowfang_Stalker(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=248

        self.name:str="Hollowfang Stalker"
        self.live:int=2
        self.power:int=3
        self.actual_live:int=2
        self.actual_power:int=3
        self.type_creature:str="Creature - Vampire Rogue"
        self.type:str="Creature"
        self.mana_cost:str="1BB"
        self.color:str="black"
        self.type_card:str="Creature - Vampire Rogue"
        self.rarity:str="Uncommon"
        self.content:str="Lifelink."
        self.image_path:str="cards/creature/Hollowfang Stalker/image.jpg"
        self.flag_dict["lifelink"]=True
