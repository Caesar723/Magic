
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Call_to_Unity(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Call to Unity"

        self.type:str="Sorcery"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Create two 1/1 white Human creature tokens."
        self.image_path:str="cards/sorcery/Call to Unity/image.jpg"


    @select_object("",1)
    async def card_ability(self,player:Player,opponent:Player,selected_object:tuple[Card]):
        for i in range(2):
            creature_tree=Call_to_Unity_Human(self.player)
            player.append_card(creature_tree,"battlefield")

class Call_to_Unity_Human(Creature):
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Human"
        self.live:int=1
        self.power:int=1
        self.actual_live:int=1
        self.actual_power:int=1

        self.type_creature:str="Creature"
        self.type:str="Creature"

        self.mana_cost:str="1"
        self.color:str="gold"
        self.type_card:str="Creature- Human"
        self.rarity:str="Uncommon"
        self.content:str=""
        self.image_path:str="cards/sorcery/Call to Unity/image.jpg"
    

    