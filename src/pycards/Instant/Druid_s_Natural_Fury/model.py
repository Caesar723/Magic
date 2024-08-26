
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object
from game.type_cards.creature import Creature



class Druid_s_Natural_Fury(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Druid's Natural Fury"

        self.type:str="Instant"

        self.mana_cost:str="3G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell. Then, create a green Beast creature token with power and toughness equal to that spell's mana cost."
        self.image_path:str="cards/Instant/Druid's Natural Fury/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        func,card=await self.undo_stack(player,opponent)
        cost=sum(card.cost.values())
        token=Druid_s_Natural_Fury_token(player,cost,cost)
        player.append_card(token,"battlefield")



class Druid_s_Natural_Fury_token(Creature):

    def __init__(self,player,live=1,power=1) -> None:
        super().__init__(player)

        self.name:str="Beast"
        self.live:int=live
        self.power:int=power
        self.actual_live:int=live
        self.actual_power:int=power

        self.type_creature:str="Beast"
        self.type:str="Creature"

        self.mana_cost:str="G"
        self.color:str="green"
        self.type_card:str="Beast"
        self.rarity:str="Rare"
        self.content:str=""
        self.image_path:str="cards/Instant/Druid's Natural Fury/image.jpg"





        