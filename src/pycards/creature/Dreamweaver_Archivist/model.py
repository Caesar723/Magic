
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Dreamweaver_Archivist(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"draw_count":1,"discard_count":1}

        self.fixed_id:int=103

        self.name:str="Dreamweaver Archivist"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Human Wizard"
        self.type:str="Creature"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Human Wizard"
        self.rarity:str="Rare"
        self.content:str="When Dreamweaver Archivist enters the battlefield, you may draw {draw_count_article} card{draw_count_plural}. If you do, discard {discard_count_article} card{discard_count_plural}."
        self.image_path:str="cards/creature/Dreamweaver Archivist/image.jpg"
        self.select_range="select|2"

    @select_object("",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        if selected_object and selected_object[0].selection_index==1 :
            for _ in range(self.effect_params["discard_count"]):
                if player.hand:
                    random_card=random.choice(player.hand)
                    player.discard(random_card)
            player.draw_card(self.effect_params["draw_count"])
            

    
    async def selection_step(self, player: "Player" = None, opponent: "Player" = None, selection_random: bool = False) -> list:
        selection1=self.create_selection("draw {draw_count_article} card{draw_count_plural} and discard {discard_count_article} card{discard_count_plural}",1)
        selection2=self.create_selection("Do nothing",2)
        card=await player.send_selection_cards([selection1,selection2],selection_random)
        
        
        return [card]
              