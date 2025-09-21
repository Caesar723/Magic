
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.buffs import StateBuff
from game.type_cards.creature import Creature


class Awaken_the_Elemental(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Awaken the Elemental"

        self.type:str="Sorcery"

        self.mana_cost:str="4GG"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Return a creature card from your graveyard to the battlefield, then put five +1/+1 counters on it until end of turn."
        self.image_path:str="cards/sorcery/Awaken the Elemental/image.jpg"


    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        die_creatures=player.get_cards_by_pos_type("graveyard",Creature)
        if die_creatures:
            creature:Creature=random.choice(die_creatures)
            new_creature=type(creature)(player)
            #player.remove_card(creature,"graveyard")
            player.append_card(new_creature,"battlefield")
            for i in range(5):
                buff_state=StateBuff(self,new_creature,1,1)
                buff_state.buff_missile="Cure"
                buff_state.color_missile="rgba(10, 50, 10, 0.9)"
                buff_state.set_end_of_turn()
                new_creature.gain_buff(buff_state,self)
        
        