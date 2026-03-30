
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.type_cards.creature import Creature
    from game.card import Card
 
from game.type_cards.land import Land
from game.type_action import actions
from game.game_function_tool import select_object


class Celestial_Haven(Land):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=166

        self.name:str="Celestial Haven"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="gold"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Celestial Haven enters the battlefield untapped and adds one white mana to your mana pool. Additionally, you may pay 3 life and tap Celestial Haven to prevent all combat damage that would be dealt this turn."
        self.image_path:str="cards/land/Celestial Haven/image.jpg"

        self.flag_dict["prevent_combat_damage"]=False

    def generate_mana(self) -> dict:
        return {"W":1}

    @select_object("",1)
    async def when_enter_landarea(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        self.tap()
        player.mana["W"]+=1
        player.action_store.add_action(actions.Change_Mana(self, player, player.get_manas()))


    async def when_clicked(self, player: "Player" = None, opponent: "Player" = None,manual:bool=False):
        if self not in player.land_area:
            return False
        if not self.get_flag("tap"):
            if not manual or self.player.life<=3:
                self.player.add_counter_dict("spend_land_count",1)
                mana=self.generate_mana()
                for key in mana:
                    player.mana[key]+=mana[key]
                self.tap()
                return True
            else:
                self.attact_to_object(player,3,"rgba(240, 248, 255, 0.85)","Missile_Hit")
                player.add_counter_dict("spend_land_count", 1)
                self.tap()
                self.flag_dict["prevent_combat_damage"]=True
                
                return True


        

        

    async def when_an_object_hert(
        self,
        object: "Player|Creature",
        value: int,
        player: "Player" = None,
        opponent: "Player" = None,
    ):
        room = self.player.room
        
        if not room.get_flag("attacker_defenders") or not self.get_flag("prevent_combat_damage"):
            return await super().when_an_object_hert(object, value, player, opponent)
        await self.cure_to_object(
            object,
            value,
            "rgba(240, 248, 255, 0.85)",
            "Missile_Hit",
        )

    async def when_end_turn(self, player: "Player" = None, opponent: "Player" = None):
        await super().when_end_turn(player, opponent)
        self.flag_dict["prevent_combat_damage"]=False
