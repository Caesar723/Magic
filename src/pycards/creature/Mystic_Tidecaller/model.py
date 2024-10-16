
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Mystic_Tidecaller(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mystic Tidecaller"
        self.live:int=3
        self.power:int=2
        self.actual_live:int=3
        self.actual_power:int=2

        self.type_creature:str="Merfolk Wizard"
        self.type:str="Creature"

        self.mana_cost:str="3U"
        self.color:str="blue"
        self.type_card:str="Merfolk Wizard"
        self.rarity:str="Mythic Rare"
        self.content:str="Flash, When Mystic Tidecaller enters the battlefield, you may return target nonland permanent to its owner's hand."
        self.image_path:str="cards/creature/Mystic Tidecaller/image.jpg"

    @select_object("all_creatures",1)
    async def when_enter_battlefield(self,player:"Player",opponent:"Player",selected_object:tuple['Card']=()):
        if selected_object:
            selected_object[0].player.remove_card(selected_object[0],"battlefield")
            new_card=type(selected_object[0])(selected_object[0].player)
            selected_object[0].player.append_card(new_card,"hand")
            

        