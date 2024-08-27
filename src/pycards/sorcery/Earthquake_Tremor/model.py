
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.type_cards.creature import Creature



class Earthquake_Tremor(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Earthquake Tremor"

        self.type:str="Sorcery"

        self.mana_cost:str="6RR"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Destroy three creature permanents randomly. For each permanent destroyed this way, create a 3/3 Elemental creature token."
        self.image_path:str="cards/sorcery/Earthquake Tremor/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ()):
        battlefield_opponent=list(opponent.battlefield)
        for i in range(3):
            if battlefield_opponent:
                print(battlefield_opponent)
                card_to_destroy=random.choice(battlefield_opponent)
                player.action_store.start_record()
                await self.destroy_object(card_to_destroy,"rgba(255,0,0,1)",'High_Missile')
                battlefield_opponent.remove(card_to_destroy)
                
                element=Earthquake_Tremor_Elemental(player)
                player.append_card(element,"battlefield")
                print(player.battlefield)
                player.action_store.end_record()
        print(player.action_store.action_list)
            



class Earthquake_Tremor_Elemental(Creature):
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Elemental"
        
        self.power:int=3
        self.live:int=3
        self.actual_live:int=3
        self.actual_power:int=3

        self.type_creature:str="Creature - Elemental"
        self.type_card:str="Creature - Elemental"
        self.type:str="Creature"

        self.color:str="red"
        self.mana_cost:str="R"
        self.rarity:str="Rare"
        self.content=""
        self.image_path:str="cards/sorcery/Earthquake Tremor/image.jpg"


        