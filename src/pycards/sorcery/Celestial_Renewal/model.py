
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
import random
from game.buffs import StateBuff


class Celestial_Renewal(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=193

        self.name:str="Celestial Renewal"

        self.type:str="Sorcery"

        self.mana_cost:str="2GW"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Celestial Renewal allows you to return 3 random creatures cards from your graveyard to the battlefield. Those creatures' stats become 1/1."
        self.image_path:str="cards/sorcery/Celestial Renewal/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        from game.type_cards.creature import Creature
        
        creatures = player.get_cards_by_pos_type("graveyard", (Creature,))
        if not creatures or len(creatures)<2:
            return
        for creature in random.sample(creatures,2):
            player.remove_card(creature, "graveyard")
            new_creature=type(creature)(player)
            org_state=new_creature.state
            buff=StateBuff(self,new_creature,1-org_state[0],1-org_state[1])
            new_creature.gain_buff(buff,self)
            player.append_card(new_creature, "battlefield")




        