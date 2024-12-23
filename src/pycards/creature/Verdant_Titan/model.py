
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

class Verdant_Titan(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Verdant Titan"
        self.live:int=5
        self.power:int=5
        self.actual_live:int=5
        self.actual_power:int=5

        self.type_creature:str="Elemental Creature"
        self.type:str="Creature"

        self.mana_cost:str="3GG"
        self.color:str="green"
        self.type_card:str="Elemental Creature"
        self.rarity:str="Mythic Rare"
        self.content:str="Trample, Vigilance, When Verdant Titan enters the battlefield or attacks, you may search your library for a land card and put it onto the battlefield tapped. If you do, shuffle your library."
        self.image_path:str="cards/creature/Verdant Titan/image.jpg"


        self.flag_dict["Trample"]=True
        self.flag_dict["Vigilance"]=True

    @select_object("",1)
    async def when_enter_battlefield(self, player: 'Player' = None, opponent: 'Player' = None, selected_object: tuple['Card'] = ...):
        self.put_land(player,opponent)
        
    async def when_start_attcak(self, card: 'Creature | Player', player: 'Player' = None, opponent: 'Player' = None):
        result= await super().when_start_attcak(card, player, opponent)
        self.put_land(player,opponent)
        return result
    
    def put_land(self,player: 'Player' = None, opponent: 'Player' = None):
        lands=player.get_cards_by_pos_type("library",(Forest,Plains,Swamp,Mountain,Island))
        if lands:
            random_land=random.choice(lands)
            player.append_card(random_land,"land_area")
            player.remove_card(random_land,"library")
            random_land.tap()
            random.shuffle(player.library)
        
        