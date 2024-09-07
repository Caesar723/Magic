
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from pycards.land.Forest.model import Forest
from pycards.land.Plains.model import Plains
from pycards.land.Island.model import Island
from pycards.land.Mountain.model import Mountain
from pycards.land.Swamp.model import Swamp

class Sage_of_the_Ancient_Grove(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Sage of the Ancient Grove"
        self.live:int=4
        self.power:int=4
        self.actual_live:int=4
        self.actual_power:int=4

        self.type_creature:str="Treefolk Creature - Treefolk"
        self.type:str="Creature"

        self.mana_cost:str="2GG"
        self.color:str="green"
        self.type_card:str="Treefolk Creature - Treefolk"
        self.rarity:str="Rare"
        self.content:str="Reach, When Sage of the Ancient Grove enters the battlefield, you may search your library for a basic land card, put it onto the battlefield tapped, then shuffle your library."
        self.image_path:str="cards/creature/Sage of the Ancient Grove/image.jpg"

        self.flag_dict["reach"]=True


    @select_object("",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        lands=player.get_cards_by_pos_type("library",(Forest,Plains,Island,Mountain,Swamp))
        if lands:
            land=lands[0]
            player.remove_card(land,"library")
            player.append_card(land,"land_area")
            land.tap()
            