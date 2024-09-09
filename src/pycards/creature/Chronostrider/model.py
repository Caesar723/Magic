
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Chronostrider(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Chronostrider"
        self.live:int=4
        self.power:int=2
        self.actual_live:int=4
        self.actual_power:int=2

        self.type_creature:str="Human Wizard"
        self.type:str="Creature"

        self.mana_cost:str="3G"
        self.color:str="green"
        self.type_card:str="Human Wizard"
        self.rarity:str="Mythic Rare"
        self.content:str="Flash, Haste. When Chronostrider enters the battlefield, you may take an extra turn after this one."
        self.image_path:str="cards/creature/Chronostrider/image.jpg"

        self.flag_dict["haste"]=True
        self.flag_dict["Flash"]=True

    @select_object("",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):

        player.add_counter_dict("extra_turn",1)
        