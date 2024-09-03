
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.type_cards.creature import Creature

class Judgment_Day(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Judgment Day"

        self.type:str="Sorcery"

        self.mana_cost:str="5WW"
        self.color:str="colorless"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Destroy all creatures. Then, each player may return one creature card from their graveyard to the battlefield."
        self.image_path:str="cards/sorcery/Judgment Day/image.jpg"


    @select_object("",1)
    async def card_ability(self,player:Player,opponent:Player,selected_object:tuple[Card]):
        for creature in player.battlefield:
            await self.destroy_object(creature,"rgba(255, 215, 0, 0.9)","Missile_Hit")
        for creature in opponent.battlefield:
            await self.destroy_object(creature,"rgba(255, 215, 0, 0.9)","Missile_Hit")
        for player_curr in [player,opponent]:
            choose_list=[]
            for card in  player_curr.graveyard:
                if isinstance(card,Creature):
                    choose_list.append(card)
            if choose_list:
                creature=random.choice(choose_list)
                player_curr.append_card(type(creature)(player_curr),"battlefield")