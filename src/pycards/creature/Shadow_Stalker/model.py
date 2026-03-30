
from __future__ import annotations
import random
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Shadow_Stalker(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Shadow Stalker"
        self.live:int=3
        self.power:int=3
        self.actual_live:int=3
        self.actual_power:int=3

        self.type_creature:str="Creature - Assassin"
        self.type:str="Creature"

        self.mana_cost:str="2BB"
        self.color:str="black"
        self.type_card:str="Creature - Assassin"
        self.rarity:str="Rare"
        self.content:str="Cannot be targeted by spells or abilities. Whenever Shadow Stalker attacks, the opponent discards a card."
        self.image_path:str="cards/creature/Shadow Stalker/image.jpg"

        self.flag_dict["Hexproof"]=True

    async def when_start_attcak(self, card: "Creature | Player", player: "Player" = None, opponent: "Player" = None):
        if opponent.hand:
            card_hand=random.choice(opponent.hand)
            opponent.discard(card_hand)
                


        return await super().when_start_attcak(card, player, opponent)


        