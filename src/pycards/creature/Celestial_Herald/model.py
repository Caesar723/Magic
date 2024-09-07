
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Celestial_Herald(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Celestial Herald"
        self.live:int=3
        self.power:int=3
        self.actual_live:int=3
        self.actual_power:int=3

        self.type_creature:str="Angel Creature"
        self.type:str="Creature"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Angel Creature"
        self.rarity:str="Mythic Rare"
        self.content:str="Flying, Lifelink. At the beginning of your upkeep, exile random nonland opponent's permanent. Return that permanent to the battlefield under its owner's control at the beginning of the next end step."
        self.image_path:str="cards/creature/Celestial Herald/image.jpg"

        self.flag_dict["flying"]=True
        self.flag_dict["lifelink"]=True

        self.creature_store=False

    async def when_start_turn(self, player: "Player" = None, opponent: "Player" = None):
        if self in player.battlefield:
            current_creature=False
            if opponent.battlefield:
                creature=random.choice(opponent.battlefield)
                await self.exile_object(creature,"rgba(239, 228, 83, 0.8)","Missile_Hit")
                current_creature=creature
            if self.creature_store:
                opponent.remove_card(self.creature_store,"exile_area")
                opponent.append_card(type(self.creature_store)(opponent),"battlefield")
            self.creature_store=current_creature
            


        