
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Celestial_Renewal(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=193

        self.name:str="Celestial Renewal"

        self.type:str="Sorcery"

        self.mana_cost:str="3GW"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Celestial Renewal allows you to return all creature cards from your graveyard to the battlefield. Those creatures gain hexproof until end of turn."
        self.image_path:str="cards/sorcery/Celestial Renewal/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        from game.type_cards.creature import Creature
        
        creatures = player.get_cards_by_pos_type("graveyard", (Creature,))
        for creature in creatures[:]:
            player.remove_card(creature, "graveyard")
            player.append_card(creature, "battlefield")




        