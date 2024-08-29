
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object


class Mage_s_Veto(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mage's Veto"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell. If that spell's mana cost is less than 3, search your library for a Sorcery card and put it into your hand."
        self.image_path:str="cards/Instant/Mage's Veto/image.jpg"
    

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        func,card=await self.undo_stack(player,opponent)
        if sum(card.cost.values())<3:
            for card in player.library:
                if card.type=="Sorcery":
                    player.append_card(card,"hand")
                    player.remove_card(card,"library")
                    break

        