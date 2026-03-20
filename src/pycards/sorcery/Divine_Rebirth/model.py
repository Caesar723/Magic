
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Divine_Rebirth(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=201

        self.name:str="Divine Rebirth"

        self.type:str="Sorcery"

        self.mana_cost:str="3W"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Return target creature card from your graveyard to the battlefield. If it's an Angel, create two 4/4 white Angel creature tokens with flying tapped and attacking."
        self.image_path:str="cards/sorcery/Divine Rebirth/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        from game.type_cards.creature import Creature
        
        creatures = player.get_cards_by_pos_type("graveyard", (Creature,))
        if creatures:
            creature = await player.send_selection_cards(creatures, selection_random=True)
            player.remove_card(creature, "graveyard")
            player.append_card(creature, "battlefield")




        