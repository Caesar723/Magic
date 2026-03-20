
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Resurgence(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=58

        self.name:str="Resurgence"

        self.type:str="Instant"

        self.mana_cost:str="3RW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Creatures you control gain double strike and lifelink until end of turn. Return target creature card with converted mana cost 3 or less from your graveyard to the battlefield."
        self.image_path:str="cards/Instant/Resurgence/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        from game.buffs import DoubleStrike, Lifelink
        from game.type_cards.creature import Creature
        
        for creature in player.battlefield:
            buff1 = DoubleStrike(self, creature)
            buff1.set_end_of_turn()
            creature.gain_buff(buff1, self)
            
            buff2 = Lifelink(self, creature)
            buff2.set_end_of_turn()
            creature.gain_buff(buff2, self)
        
        creatures = player.get_cards_by_pos_type("graveyard", (Creature,))
        if creatures:
            creature = await player.send_selection_cards(creatures, selection_random=True)
            player.remove_card(creature, "graveyard")
            player.append_card(creature, "battlefield")




        