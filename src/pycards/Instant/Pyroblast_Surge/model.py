
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Pyroblast_Surge(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"damage":3,"damage_bonus":1}

        self.fixed_id:int=56

        self.name:str="Pyroblast Surge"

        self.type:str="Instant"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Pyroblast Surge deals {damage} damage to target creature or player. If you control an untaped Mountain, Pyroblast Surge deals {damage_bonus} additional damage."
        self.image_path:str="cards/Instant/Pyroblast Surge/image.jpg"

    @select_object("all_roles",1)
    async def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        if selected_object:
            power=self.effect_params["damage"]
            for land in player.land_area:
                if not land.get_flag("tap"):
                    power=self.effect_params["damage"]+self.effect_params["damage_bonus"]
            player.action_store.start_record()
            await self.attact_to_object(selected_object[0],power,"rgba(243, 0, 0, 0.9)","Missile_Hit")
            player.action_store.end_record()

            


        