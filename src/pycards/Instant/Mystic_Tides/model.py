
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
import random


class Mystic_Tides(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mystic Tides"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Counter target creature spell unless its controller's mana pool is less than 2. If it is countered this way, tap random opponent's creature."
        self.image_path:str="cards/Instant/Mystic Tides/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        stack=player.room.stack
        if not stack:
            return
        func,card=stack[-1]
        if card.player!=opponent or card.type!="Creature":
            return
        if not card.player.check_can_use({"colorless":2,"U":0,"W":0,"B":0,"R":0,"G":0})[0]:
            stack.pop()
            if card in opponent.battlefield:
                await self.destroy_object(card, "rgba(90,120,255,0.9)", "Missile_Hit")
            if opponent.battlefield:
                creature=random.choice(opponent.battlefield)
                creature.tap()

