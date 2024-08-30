
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object


class Warrior_s_Forced_Challenge(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Warrior's Forced Challenge"

        self.type:str="Instant"

        self.mana_cost:str="2R"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Counter target creature spell. Another target creature fights a creature you control."
        self.image_path:str="cards/Instant/Warrior's Forced Challenge/image.jpg"

        self.undo_range="Creature"


    @select_object("opponent_creatures",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        func,card = await self.undo_stack(player,opponent)
        if selected_object and player.battlefield and card!=selected_object[0]:
            creature=random.choice(player.battlefield)
            await selected_object[0].fight_to_creature(creature)
            

        