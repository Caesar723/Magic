
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
import random

class Resurgence(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=58

        self.name:str="Resurgence"

        self.type:str="Instant"

        self.mana_cost:str="2RW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Creatures you control gain double strike and lifelink until end of turn. Return random creature card with converted mana cost 3 or less from your graveyard to the battlefield."
        self.image_path:str="cards/Instant/Resurgence/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        from game.buffs import KeyBuff
        from game.type_cards.creature import Creature
        
        for creature in player.battlefield:
            buff1 = KeyBuff(self, creature,"Double strike")
            buff1.set_end_of_turn()
            creature.gain_buff(buff1, self)
            
            buff2 = KeyBuff(self, creature,"lifelink")
            buff2.set_end_of_turn()
            creature.gain_buff(buff2, self)
        
        creatures = player.get_cards_by_pos_type("graveyard", (Creature,))
        if creatures:
            candidate_creatures = [c for c in creatures if c.cost["colorless"]<=3]
            if not candidate_creatures:
                return
            
            creature = random.choice(candidate_creatures)
            player.remove_card(creature,"graveyard")
            player.remove_card(creature, "graveyard")
            player.append_card(type(creature)(player), "battlefield")




        