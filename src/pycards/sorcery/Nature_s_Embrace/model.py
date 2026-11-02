
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
import random

class Nature_s_Embrace(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"creature_power":4,"creature_toughness":4}

        self.fixed_id:int=224

        self.name:str="Nature's Embrace"

        self.type:str="Sorcery"

        self.mana_cost:str="3G"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Search your library for a creature card and put it onto the battlefield tapped, the state of the creature is {creature_power}/{creature_toughness}. Then shuffle your library."
        self.image_path:str="cards/sorcery/Nature's Embrace/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        from game.type_cards.creature import Creature
        
        creatures = player.get_cards_by_pos_type("library", (Creature,))
        if creatures:
            creature = random.choice(creatures)
            player.remove_card(creature, "library")
            new_creature=creature.copy_for_player(player)
            new_creature.live=self.effect_params["creature_toughness"]
            new_creature.power=self.effect_params["creature_power"]
            new_creature.actual_live=self.effect_params["creature_toughness"]
            new_creature.actual_power=self.effect_params["creature_power"]
            player.append_card(new_creature, "battlefield")
            creature.tap()




        