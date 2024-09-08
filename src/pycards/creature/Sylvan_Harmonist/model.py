
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from pycards.land.Forest.model import Forest
from pycards.land.Plains.model import Plains
from pycards.land.Swamp.model import Swamp
from pycards.land.Mountain.model import Mountain
from pycards.land.Island.model import Island

class Sylvan_Harmonist(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Sylvan Harmonist"
        self.live:int=3
        self.power:int=2
        self.actual_live:int=3
        self.actual_power:int=2

        self.type_creature:str="Human Druid"
        self.type:str="Creature"

        self.mana_cost:str="1GG"
        self.color:str="green"
        self.type_card:str="Human Druid"
        self.rarity:str="Rare"
        self.content:str="When Sylvan Harmonist enters the battlefield, you may search your library for a basic land card and put it onto the battlefield tapped. If you do, shuffle your library."
        self.image_path:str="cards/creature/Sylvan Harmonist/image.jpg"

    @select_object("",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        lands=player.get_cards_by_pos_type("library",(Forest,Plains,Swamp,Mountain,Island))
        if lands:
            random_land=random.choice(lands)
            player.append_card(random_land,"land_area")
            player.remove_card(random_land,"library")
            random_land.tap()
            random.shuffle(player.library)
        