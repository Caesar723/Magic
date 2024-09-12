
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

class Verdant_Wyrm(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Verdant Wyrm"
        self.live:int=4
        self.power:int=4
        self.actual_live:int=4
        self.actual_power:int=4

        self.type_creature:str="Dragon Creature - Dragon"
        self.type:str="Creature"

        self.mana_cost:str="3GG"
        self.color:str="green"
        self.type_card:str="Dragon Creature - Dragon"
        self.rarity:str="Rare"
        self.content:str="Trample, When Verdant Wyrm enters the battlefield, you may search your library for a land card, put it onto the battlefield tapped, then shuffle your library."
        self.image_path:str="cards/creature/Verdant Wyrm/image.jpg"
        self.flag_dict["Trample"]=True
        
    @select_object("",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        lands=player.get_cards_by_pos_type("library",(Forest,Plains,Swamp,Mountain,Island))
        if lands:
            random_land=random.choice(lands)
            player.append_card(random_land,"land_area")
            player.remove_card(random_land,"library")
            random_land.tap()
            random.shuffle(player.library)

        