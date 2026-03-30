
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Rift_in_Reality(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=226

        self.name:str="Rift in Reality"

        self.type:str="Sorcery"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Rift in Reality allows you to exile target creature. Return it to the battlefield under its owner's control at the beginning of the next end step.When it returns, its owner draws a card."
        self.image_path:str="cards/sorcery/Rift in Reality/image.jpg"

        self.exiled_creature=None

    @select_object("opponent_creatures",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if selected_object:
            target = selected_object[0]
            await self.exile_object(target, "rgba(239, 228, 83, 0.8)", "Missile_Hit")
            self.exiled_creature=target

    async def when_start_turn(self, player: "Player" = None, opponent: "Player" = None):
        if self.exiled_creature is not None:
            new_creature=type(self.exiled_creature)(self.exiled_creature.player)
            self.exiled_creature.player.append_card(new_creature,"battlefield")
            self.exiled_creature.player.draw_card(1)
            self.exiled_creature=None
            player.remove_card_from_dict("start_turn",self)
        return await super().when_start_turn(player, opponent)





        