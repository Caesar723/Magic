
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.buffs import Tap

class Nyxborn_Serpent(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Nyxborn Serpent"
        self.live:int=3
        self.power:int=3
        self.actual_live:int=3
        self.actual_power:int=3

        self.type_creature:str="Enchantment Creature - Serpent"
        self.type:str="Creature"

        self.mana_cost:str="4U"
        self.color:str="blue"
        self.type_card:str="Enchantment Creature - Serpent"
        self.rarity:str="Uncommon"
        self.content:str="Constellation - Whenever Nyxborn Serpent enters the battlefield under your control, you may tap target creature an opponent controls."
        self.image_path:str="cards/creature/Nyxborn Serpent/image.jpg"


    @select_object("opponent_creatures",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if selected_object:
            buff=Tap(self,selected_object[0])
            selected_object[0].gain_buff(buff,self)
        