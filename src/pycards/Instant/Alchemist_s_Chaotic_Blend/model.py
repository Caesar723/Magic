
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object
from game.type_cards.sorcery import Sorcery

class Alchemist_s_Chaotic_Blend(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Alchemist's Chaotic Blend"

        self.type:str="Instant"

        self.mana_cost:str="3R"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell. Then reveal a random card from your library and cast it without paying its mana cost."
        self.image_path:str="cards/Instant/Alchemist's Chaotic Blend/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:Player,opponent:Player,selected_object:tuple[Card]):
        func,card_stack=await self.undo_stack(player,opponent)

        cards_lib=player.get_cards_by_pos_type("library",(Instant,Sorcery),except_type=(Instant_Undo,))
        if cards_lib:
            card_lib:"Instant|Sorcery"=random.choice(cards_lib)
            player.remove_card(card_lib,"library")
            new_func=await card_lib.card_ability(player,opponent,auto_select=True)
            self.stack.append((new_func,card_lib))
        