
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Demonic_Ascendance(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=197

        self.name:str="Demonic Ascendance"

        self.type:str="Sorcery"

        self.mana_cost:str="3B"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Target opponent reveals their hand. You may choose a creature card from it and put it onto the battlefield under your control. That creature gains haste. Sacrifice it at the beginning of the next end step."
        self.image_path:str="cards/sorcery/Demonic Ascendance/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        from game.type_cards.creature import Creature
        
        creatures = [c for c in opponent.hand if isinstance(c, Creature)]
        if creatures:
            creature = await opponent.send_selection_cards(creatures, selection_random=True)
            opponent.remove_card(creature, "hand")
            player.append_card(creature, "battlefield")




        