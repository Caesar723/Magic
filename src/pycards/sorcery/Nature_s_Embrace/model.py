
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Nature_s_Embrace(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=224

        self.name:str="Nature's Embrace"

        self.type:str="Sorcery"

        self.mana_cost:str="3G"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Search your library for a creature card and put it onto the battlefield tapped. Then shuffle your library."
        self.image_path:str="cards/sorcery/Nature's Embrace/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        from game.type_cards.creature import Creature
        
        creatures = player.get_cards_by_pos_type("library", (Creature,))
        if creatures:
            creature = await player.send_selection_cards(creatures, selection_random=True)
            player.remove_card(creature, "library")
            player.append_card(creature, "battlefield")
            creature.tap()




        