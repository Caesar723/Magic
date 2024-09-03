
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object
from game.type_cards.creature import Creature
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery

class Necromancer_s_Soul_Seize(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Necromancer's Soul Seize"

        self.type:str="Instant"

        self.mana_cost:str="2B"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target creature spell. If the spell is countered this way, exile a card from your library, then return a card of the same type from your graveyard to your hand."
        self.image_path:str="cards/Instant/Necromancer's Soul Seize/image.jpg"

        self.undo_range:str="Creature"

    @select_object("",1)
    async def card_ability(self,player:Player,opponent:Player,selected_object:tuple[Card]):
        func,card_stack=await self.undo_stack(player,opponent)
        type_tuple=(Creature,Land,Sorcery,Instant)

        if player.library:
            lib_card=random.choice(player.library)
            player.remove_card(lib_card,"library")
            player.append_card(lib_card,"exile_area")

            for type_card in type_tuple:
                if isinstance(lib_card,type_card):
                    break
            card_random_list=player.get_cards_by_pos_type("graveyard",(type_card))

            if card_random_list:
                card_random=random.choice(card_random_list)
                new_card=type(card_random)(player)
                player.remove_card(card_random,"graveyard")
                player.append_card(new_card,"hand")
        
        


        