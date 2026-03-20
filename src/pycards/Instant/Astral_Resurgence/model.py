
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
from game.type_cards.creature import Creature
from game.buffs import KeyBuff


class Astral_Resurgence(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=7

        self.name:str="Astral Resurgence"

        self.type:str="Instant"

        self.mana_cost:str="1WW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Return a creature cards from your graveyard to the battlefield. It gains lifelink until end of turn."
        self.image_path:str="cards/Instant/Astral Resurgence/image.jpg"


    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        die_creatures=player.get_cards_by_pos_type("graveyard",Creature)
        if die_creatures:
            creature:Creature=random.choice(die_creatures)
            new_creature=type(creature)(player)
            #player.remove_card(creature,"graveyard")
            player.append_card(new_creature,"battlefield")
            buff_key=KeyBuff(self,new_creature,"lifelink")
            buff_key.set_end_of_turn()
            new_creature.gain_buff(buff_key,self)