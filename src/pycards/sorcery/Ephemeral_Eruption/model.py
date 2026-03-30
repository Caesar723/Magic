
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
    from game.type_cards.creature import Creature
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Ephemeral_Eruption(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Ephemeral Eruption"

        self.type:str="Sorcery"

        self.mana_cost:str="1RR"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Ephemeral Eruption deals 4 damage to each creature. At the beginning of the next end step, return all creatures killed by this way to the battlefield under their owner's control."
        self.image_path:str="cards/sorcery/Ephemeral Eruption/image.jpg"

        self.dead_creatures:list["Creature"]=[]

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        all_creatures = list(player.battlefield) + list(opponent.battlefield)

        for creature in all_creatures:
            await self.attact_to_object(creature, 4, "rgba(255,0,0,1)", "Missile_Hit")
            check_dead=await creature.check_dead()
            if check_dead:
                self.dead_creatures.append(creature)
        
    async def when_end_turn(self, player: "Player" = None, opponent: "Player" = None):
        if self.dead_creatures:
            for creature in self.dead_creatures:
                creature.player.append_card(type(creature)(creature.player),"battlefield")
            self.dead_creatures=[]

            player.remove_card_from_dict("end_step",self)


        