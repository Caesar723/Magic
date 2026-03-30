
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
    from game.type_cards.creature import Creature
 
from game.type_cards.land import Land
from game.type_action import actions
from game.game_function_tool import select_object

class Luminous_Glade(Land):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=170

        self.name:str="Luminous Glade"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="gold"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Luminous Glade enters the battlefield tapped and adds one white mana to your mana pool. You may tap Luminous Glade to prevent the next 1 damage that would be dealt to target creature or player this turn."
        self.image_path:str="cards/land/Luminous Glade/image.jpg"
        self.flag_dict["prevent_next_damage"]=False

    def generate_mana(self) -> dict:
        return {"W":1}

    @select_object("", 1)
    async def when_enter_landarea(self,player: "Player" = None,opponent: "Player" = None,selected_object: tuple = (),**kwargs):
        self.tap()
        player.mana["W"] += 1
        player.action_store.add_action(actions.Change_Mana(self, player, player.get_manas()))

    

    async def when_clicked(self, player: "Player" = None, opponent: "Player" = None,manual:bool=False):
        if self not in player.land_area:
            return False
        if self.get_flag("tap"):
            return False

        self.player.add_counter_dict("spend_land_count",1)
        self.tap()
        if not manual:
            
            mana=self.generate_mana()
            for key in mana:
                player.mana[key]+=mana[key]
            
            return True
        else:

            self.flag_dict["prevent_next_damage"] = True

            return True


    async def when_an_object_hert(
        self,
        object: "Player|Creature",
        value: int,
        player: "Player" = None,
        opponent: "Player" = None,
    ):
        if value <= 0 or not self.get_flag("prevent_next_damage"):
            return await super().when_an_object_hert(object, value, player, opponent)
        prevent = min(1, value)
        await self.cure_to_object(
            object,
            prevent,
            "rgba(255, 255, 230, 0.75)",
            "Missile_Hit",
        )
        self.flag_dict["prevent_next_damage"] = False

    async def when_end_turn(self, player: "Player" = None, opponent: "Player" = None):
        await super().when_end_turn(player, opponent)
        self.flag_dict["prevent_next_damage"] = False
