
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object


class Mechanist_s_Disruption_Device(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Mechanist's Disruption Device"

        self.type:str="Instant"

        self.mana_cost:str="3U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Counter target spell. Then draw a card and you may put a land card from your hand onto the battlefield."
        self.image_path:str="cards/Instant/Mechanist's Disruption Device/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:Player,opponent:Player, selected_object: tuple["Card"] = ...):
        func,card=await self.undo_stack(player,opponent)
        player.draw_card(1)

        lands=[]
       
        for card in player.hand:
            if card.type=="Land":
                lands.append(card)

        if lands:
            card=random.choice(lands)
            player.append_card(card,"land_area")
            player.remove_card(card,"hand")
            

        

        



        