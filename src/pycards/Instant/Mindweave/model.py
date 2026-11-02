
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant_Undo
from game.game_function_tool import select_object


class Mindweave(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"draw_count":1,"mana_threshold":2}

        self.name:str="Mindweave"

        self.type:str="Instant"

        self.mana_cost:str="UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell unless its controller's mana pool is less than {mana_threshold}. If that spell is countered this way, you may draw {draw_count} cards."
        self.image_path:str="cards/Instant/Mindweave/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        
        if not opponent.check_can_use({"colorless":self.effect_params["mana_threshold"],"U":0,"W":0,"B":0,"R":0,"G":0})[0]:
            func, card = await self.undo_stack(player, opponent)
            player.draw_card(self.effect_params["draw_count"])




        