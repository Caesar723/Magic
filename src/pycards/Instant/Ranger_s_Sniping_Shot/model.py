
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object
from game.type_cards.creature import Creature

class Ranger_s_Sniping_Shot(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Ranger's Sniping Shot"

        self.type:str="Instant"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell. If that spell is a creature spell, deal damage to its controller equal to that creature's power."
        self.image_path:str="cards/Instant/Ranger's Sniping Shot/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        func,card = await self.undo_stack(player,opponent)
        if isinstance(card,Creature):
            power,life=card.state
            await self.attact_to_object(card.player,power,"rgba(144, 238, 144, 0.9)","Missile_Hit")
       

        