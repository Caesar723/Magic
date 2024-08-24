
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from pycards.land.Forest.model import Forest

class Guardian_of_the_Grove__(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Guardian of the Grove"
        self.live:int=3
        self.power:int=3
        self.actual_live:int=3
        self.actual_power:int=3

        self.type_creature:str="Elemental Creature"
        self.type:str="Creature"

        self.mana_cost:str="1WW"
        self.color:str="colorless"
        self.type_card:str="Elemental Creature"
        self.rarity:str="Uncommon"
        self.content:str="Whenever Guardian of the Grove enters the battlefield, you may search your library for a basic Forest card and put it onto the battlefield tapped."
        self.image_path:str="cards/creature/Guardian of the Grove  /image.jpg"
    @select_object("",1)
    async def when_enter_battlefield(self,player: "Player" = None,opponent: "Player" = None,selected_object:tuple['Card']=()):
        for card in player.library:
            if isinstance(card,Forest):
                player.remove_card(card,"library")
                player.append_card(card,"battlefield")
                card.tap()
                break
        

        