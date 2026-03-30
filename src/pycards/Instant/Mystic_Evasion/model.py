
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Mystic_Evasion(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=37

        self.name:str="Mystic Evasion"

        self.type:str="Instant"

        self.mana_cost:str="1UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Return target attacking creature to its owner's hand. Draw a card."
        self.image_path:str="cards/Instant/Mystic Evasion/image.jpg"


    @select_object("",1)
    async def card_ability(self,player:Player,opponent:Player,selected_object:tuple[Card]):
        if player.room.attacker:
            if player.room.attacker in opponent.battlefield or player.room.attacker in player.battlefield:
                player.room.attacker.player.remove_card(player.room.attacker,"battlefield")

                new_card=type(player.room.attacker)(player.room.attacker.player)
                player.room.attacker.player.append_card(new_card,"hand")

        player.draw_card(1)
        
        