
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object


class Thunderstrike(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Thunderstrike"

        self.type:str="Sorcery"

        self.mana_cost:str="3RR"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Choose one creature. Thunderstrike deals 8 damage to that creature. If that creature dies, Thunderstrike deals the same amount of damage to each opponent."
        self.image_path:str="cards/sorcery/Thunderstrike/image.jpg"

    @select_object("all_creatures",1)
    async def card_ability(self, player: "Player", opponent: "Player", selected_object: tuple["Card"]):
        if selected_object:
            damage=8
            player.action_store.start_record()
            await self.attact_to_object(selected_object[0],damage,"rgba(255,0,0,1)","Missile_Hit")
            life=selected_object[0].state[1]
            if await selected_object[0].check_dead() and life<=0:
                damage+=life
                player.action_store.start_record()
                for creature in opponent.battlefield:
                    if creature!=selected_object[0]:
                        await self.attact_to_object(creature,damage,"rgba(255,0,0,1)","Missile_Hit")
                await self.attact_to_object(opponent,damage,"rgba(255,0,0,1)","Missile_Hit")
                player.action_store.end_record()
            player.action_store.end_record()

        