
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
from game.type_cards.creature import Creature
from game.type_cards.instant import Instant_Undo
from game.game_function_tool import select_object


class Mystic_Confluence(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mystic Confluence"

        self.type:str="Instant"

        self.mana_cost:str="5U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Counter target spell. Return target creature to its owner's hand. Draw a card."
        self.image_path:str="cards/Instant/Mystic Confluence/image.jpg"

    @select_object("all_creatures",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        func,card=await self.undo_stack(player,opponent)
        if selected_object:
            target=selected_object[0]
            if isinstance(target,Creature):
                target.player.remove_card(target,"battlefield")
                target.player.append_card(type(target)(target.player),"hand")
        player.draw_card(1)




        