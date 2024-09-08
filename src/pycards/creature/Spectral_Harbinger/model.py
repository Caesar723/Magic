
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Spectral_Harbinger(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Spectral Harbinger"
        self.live:int=3
        self.power:int=2
        self.actual_live:int=3
        self.actual_power:int=2

        self.type_creature:str="Spirit Creature - Spirit"
        self.type:str="Creature"

        self.mana_cost:str="2WW"
        self.color:str="gold"
        self.type_card:str="Spirit Creature - Spirit"
        self.rarity:str="Rare"
        self.content:str="Flying, Lifelink (Damage dealt by this creature also causes you to gain that much life), When Spectral Harbinger enters the battlefield, you may exile random creature card from a graveyard. If you do, you gain 2 life."
        self.image_path:str="cards/creature/Spectral Harbinger/image.jpg"

        self.flag_dict['lifelink']=True
        self.flag_dict['flying']=True

    @select_object("",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        graveyard_creatures=player.get_cards_by_pos_type("graveyard",(Creature,))
        if graveyard_creatures:
            random_creature=random.choice(graveyard_creatures)
            player.remove_card(random_creature,"graveyard")
            await self.cure_to_object(player,2,"rgba(255, 215, 0, 0.9)",'Missile_Hit')
            



        