
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from game.buffs import StateBuff,KeyBuff
from pycards.land.Forest.model import Forest
from pycards.land.Plains.model import Plains
from pycards.land.Swamp.model import Swamp
from pycards.land.Mountain.model import Mountain
from pycards.land.Island.model import Island
import random

class Wild_Growth_Rush(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=86

        self.name:str="Wild Growth Rush"

        self.type:str="Instant"

        self.mana_cost:str="1GG"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Target creature gains +2/+2 and trample until end of turn. Then, if you control a Forest, you may search your library for a basic land card and put it onto the battlefield tapped."
        self.image_path:str="cards/Instant/Wild Growth Rush/image.jpg"


    @select_object("all_creatures",1)
    async def card_ability(self,player:Player,opponent:Player,selected_object:tuple[Card]):
        if selected_object:
            buff=StateBuff(self,selected_object[0],2,2)
            buff.set_end_of_turn()
            selected_object[0].gain_buff(buff,self)
            buff=KeyBuff(self,selected_object[0],"Trample")
            buff.set_end_of_turn()
            selected_object[0].gain_buff(buff,self)
        
        if player.get_cards_by_pos_type("land_area",(Forest)):
            self.put_land(player,opponent)
        


    def put_land(self,player: 'Player' = None, opponent: 'Player' = None):
        lands=player.get_cards_by_pos_type("library",(Forest,Plains,Swamp,Mountain,Island))
        if lands:
            random_land=random.choice(lands)
            player.append_card(random_land,"land_area")
            player.remove_card(random_land,"library")
            random_land.tap()
            random.shuffle(player.library)
        