
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Divine_Reckoning(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=202

        self.name:str="Divine Reckoning"

        self.type:str="Sorcery"

        self.mana_cost:str="4W"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Destroy all non-angel creatures. Each player gains life equal to the number of creatures they controlled that were destroyed this way."
        self.image_path:str="cards/sorcery/Divine Reckoning/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        all_creatures = list(player.battlefield) + list(opponent.battlefield)
        destroyed_count = {player: 0, opponent: 0}
        
        for creature in all_creatures:
            if 'Angel' not in getattr(creature, 'type_creature', ''):
                owner = creature.player
                await self.destroy_object(creature, "rgba(255,0,0,0.5)", "Missile_Hit")
                destroyed_count[owner] += 1
        
        await self.cure_to_object(player, destroyed_count[player], "rgba(0,255,0,1)", "Cure")
        await self.cure_to_object(opponent, destroyed_count[opponent], "rgba(0,255,0,1)", "Cure")




        