
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object
from game.type_cards.creature import Creature

class Summoner_s_Arcane_Acquisition(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Summoner's Arcane Acquisition"

        self.type:str="Instant"

        self.mana_cost:str="2G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell. If the spell is countered this way, create an Elemental creature token with power and toughness equal to that spell's mana cost."
        self.image_path:str="cards/Instant/Summoner's Arcane Acquisition/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:"Player",opponent:"Player",selected_object:tuple["Card"]):
        func,card=await self.undo_stack(player,opponent)
        
        cost=sum(card.cost.values())

        class Summoner_s_Arcane_Acquisition_Token(Creature):
            def __init__(self,player) -> None:
                super().__init__(player)

                self.name:str="Elemental Token"
                self.live:int=cost
                self.power:int=cost
                self.actual_live:int=cost
                self.actual_power:int=cost

                self.type_creature:str="Creature - Elemental"
                self.type:str="Creature"
                self.mana_cost:str="G"
                self.color:str="green"
                self.type_card:str="Creature - Elemental"
                self.rarity:str="Rare"
                self.content:str=""
                self.image_path:str="cards/Instant/Summoner's Arcane Acquisition/image.jpg"

        card=Summoner_s_Arcane_Acquisition_Token(player)
        player.append_card(card,"battlefield")
    