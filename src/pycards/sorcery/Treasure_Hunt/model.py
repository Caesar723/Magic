
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Treasure_Hunt(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=237

        self.name:str="Treasure Hunt"

        self.type:str="Sorcery"

        self.mana_cost:str="U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Reveal the top X cards of your library. Put all land cards revealed this way into your hand and the rest on the bottom of your library in any order."
        self.image_path:str="cards/sorcery/Treasure Hunt/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        from game.type_cards.land import Land
        
        revealed = []
        for _ in range(min(5, len(player.library))):
            if player.library:
                card = player.library[0]
                revealed.append(card)
                player.remove_card(card, "library")
                
                if isinstance(card, Land):
                    player.append_card(card, "hand")
                else:
                    player.append_card(card, "graveyard")




        