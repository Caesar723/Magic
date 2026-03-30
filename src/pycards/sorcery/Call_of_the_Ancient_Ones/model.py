
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Call_of_the_Ancient_Ones(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=186

        self.name:str="Call of the Ancient Ones"

        self.type:str="Sorcery"

        self.mana_cost:str="2BB"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Call of the Ancient Ones allows you to return random creature card from a graveyard to the battlefield under your control. That creature gains haste until end of turn and must be sacrificed at the beginning of the next end step."
        self.image_path:str="cards/sorcery/Call of the Ancient Ones/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        from game.type_cards.creature import Creature
        import random
        
        all_graveyards = player.graveyard + opponent.graveyard
        creatures = [c for c in all_graveyards if isinstance(c, Creature)]
        
        if creatures:
            creature = random.choice(creatures)
            if creature in player.graveyard:
                player.remove_card(creature, "graveyard")
            else:
                opponent.remove_card(creature, "graveyard")
            player.append_card(creature, "battlefield")




        