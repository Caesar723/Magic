
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.type_action.actions import Change_Mana

class Essence_Channeler(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Essence Channeler"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Human Shaman"
        self.type:str="Creature"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Human Shaman"
        self.rarity:str="Rare"
        self.content:str="Whenever you cast a creature spell, you may add G to your mana pool."
        self.image_path:str="cards/creature/Essence Channeler/image.jpg"

    async def when_play_a_card(self,card:'Card',player:'Player'=None,opponent:'Player'=None):
        if isinstance(card,Creature) and self in player.battlefield:
            player.mana["G"]+=1
            player.action_store.add_action(Change_Mana(self,player,player.get_manas()))
            

        

        