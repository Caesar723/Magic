
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Pious_Courser(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Pious Courser"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Human Cleric"
        self.type:str="Creature"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Human Cleric"
        self.rarity:str="Common"
        self.content:str="When Pious Courser enters the battlefield, you gain 2 life."
        self.image_path:str="cards/creature/Pious Courser/image.jpg"

    @select_object("",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        await self.cure_to_object(player,2,"rgba(245, 238, 145, 0.8)","Missile_Hit")