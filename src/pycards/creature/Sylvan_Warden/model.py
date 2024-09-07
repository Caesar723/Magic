
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
from pycards.land.Island.model import Island
from pycards.land.Mountain.model import Mountain
from pycards.land.Swamp.model import Swamp
from game.buffs import StateBuff


class Sylvan_Warden(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Sylvan Warden"
        self.live:int=4
        self.power:int=2
        self.actual_live:int=4
        self.actual_power:int=2

        self.type_creature:str="Elf Shaman"
        self.type:str="Creature"

        self.mana_cost:str="4G"
        self.color:str="green"
        self.type_card:str="Elf Shaman"
        self.rarity:str="Rare"
        self.content:str="When Sylvan Warden enters the battlefield, you may search your library for a basic land card and put it onto the battlefield tapped. If you do, shuffle your library.Whenever Sylvan Warden attacks, you may put a +1/+1 counter on target creature you control."
        self.image_path:str="cards/creature/Sylvan Warden/image.jpg"


    @select_object("",1)
    async def when_enter_battlefield(self,player:"Player",opponent:"Player",selected_object:tuple['Card']=()):
        lands=player.get_cards_by_pos_type("library",(Forest,Plains,Island,Mountain,Swamp))
        if lands:
            land=lands[0]
            player.remove_card(land,"library")
            player.append_card(land,"land_area")
            land.tap()

    async def when_start_attcak(self,defender:Creature,player:Player,opponent:Player):
        if player.battlefield:
            creature=random.choice(player.battlefield)
            buff=StateBuff(self,creature,1,1)
            creature.gain_buff(buff,self)
        
            

        