
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.type_cards.creature import Creature

class Falling_Stars(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Falling Stars"

        self.type:str="Sorcery"

        self.mana_cost:str="7RR"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Deal 7 damage to all creatures, then summon a 7/7 Star Beast creature token onto the battlefield."
        self.image_path:str="cards/sorcery/Falling Stars/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ()):
        colors = ("rgba(255, 165, 0, 0.9)", "rgba(255, 215, 0, 0.8)", "rgba(255, 69, 0, 0.9)", "rgba(255, 140, 0, 0.8)", "rgba(255, 99, 71, 0.8)")
        player.action_store.start_record()
        for creature_opponent in opponent.battlefield:
            await self.attact_to_object(creature_opponent,7,random.choice(colors),"Missile_Hit")
        for creature_self in player.battlefield:
            await self.attact_to_object(creature_self,7,random.choice(colors),"Missile_Hit")
        player.action_store.end_record()

        player.action_store.start_record()
        star_beast=Falling_Stars_Star_Beast(player)
        player.append_card(star_beast,"battlefield")
        player.action_store.end_record()


class Falling_Stars_Star_Beast(Creature):
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Star Beast"
        self.type:str="Creature"
        self.power:int=7
        self.live:int=7
        self.actual_live:int=7
        self.actual_power:int=7

        self.type_creature:str="Creature - Star"
        self.type_card:str="Creature - Star"
        self.type:str="Creature"

        self.color:str="red"
        self.mana_cost:str="R"
        self.rarity:str="Rare"
        self.content:str=""
        self.image_path:str="cards/sorcery/Falling Stars/image.jpg"



        