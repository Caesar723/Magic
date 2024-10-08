
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Shadowtide_Leviathan(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Shadowtide Leviathan"
        self.live:int=8
        self.power:int=8
        self.actual_live:int=8
        self.actual_power:int=8

        self.type_creature:str="Leviathan Creature - Leviathan"
        self.type:str="Creature"

        self.mana_cost:str="5UUU"
        self.color:str="blue"
        self.type_card:str="Leviathan Creature - Leviathan"
        self.rarity:str="Mythic Rare"
        self.content:str="Islandwalk (This creature can't be blocked as long as defending player controls an Island), When Shadowtide Leviathan enters the battlefield, you may return target nonland permanent an opponent controls to its owner's hand."
        self.image_path:str="cards/creature/Shadowtide Leviathan/image.jpg"

        self.flag_dict["Islandwalk"]=True

        
    @select_object("opponent_creatures",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if selected_object:
            new_card=type(selected_object[0])(opponent)
            opponent.remove_card(selected_object[0],"battlefield")
            opponent.append_card(new_card,"hand")