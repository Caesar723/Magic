
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

class Thornroot_Druid(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Thornroot Druid"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Elf Druid"
        self.type:str="Creature"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Elf Druid"
        self.rarity:str="Uncommon"
        self.content:str="When Thornroot Druid enters the battlefield, you may search your library for a basic land card, reveal it, put it into your hand, then shuffle your library."
        self.image_path:str="cards/creature/Thornroot Druid/image.jpg"

    @select_object("",1)
    async def when_enter_battlefield(self,player:"Player",opponent:"Player",selected_object:tuple['Card']=()):
        basic_lands=player.get_cards_by_pos_type("library",(Plains,Swamp,Mountain,Island,Forest))
        if basic_lands:
            land=random.choice(basic_lands)
            player.remove_card(land,"library")
            player.append_card(land,"hand")
            random.shuffle(player.library)


        