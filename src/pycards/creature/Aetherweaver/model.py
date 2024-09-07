
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.type_cards.instant import Instant
from game.type_cards.sorcery import Sorcery


class Aetherweaver(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Aetherweaver"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Human Wizard"
        self.type:str="Creature"

        self.mana_cost:str="3U"
        self.color:str="blue"
        self.type_card:str="Human Wizard"
        self.rarity:str="Mythic Rare"
        self.content:str="When Aetherweaver enters the battlefield, look at the top three cards of your library. You may put an instant or sorcery card from among them into your hand. Put the rest on the bottom of your library in any order."
        self.image_path:str="cards/creature/Aetherweaver/image.jpg"

    @select_object("",1)
    async def when_enter_battlefield(self,player:"Player",opponent:"Player",selected_object:tuple['Card']=()):
        cards=player.get_cards_by_pos_type("library",(Instant,Sorcery))
        if len(cards)>=3:
            cards_selection=cards[0:3]
        elif cards:
            cards_selection=cards[0:len(cards)]
        else:
            return
        card=await player.send_selection_cards(cards_selection,selection_random=True)
        player.append_card(card,"hand")
        player.remove_card(card,"library")

        cards_selection.remove(card)
        for other_card in cards_selection:
            player.remove_card(other_card,"library")
            player.append_card(other_card,"library")
            
            