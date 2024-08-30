
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object


class Priest_s_Divine_Binding(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Priest's Divine Binding"

        self.type:str="Instant"

        self.mana_cost:str="2W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Counter target creature spell. You gain life equal to that creature's power."
        self.image_path:str="cards/Instant/Priest's Divine Binding/image.jpg"

        self.undo_range="Creature"


    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        func,card = await self.undo_stack(player,opponent)
        power,life=card.state
        await self.cure_to_object(player,power,"rgba(144, 238, 144, 0.9)","Missile_Hit")
        

        