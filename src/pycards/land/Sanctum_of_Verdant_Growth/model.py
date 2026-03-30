
from __future__ import annotations
import random
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.land import Land
from pycards.land.Forest.model import Forest
from game.game_function_tool import select_object
from game.type_action import actions


class Sanctum_of_Verdant_Growth(Land):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=176

        self.name:str="Sanctum of Verdant Growth"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="green"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Sanctum of Verdant Growth enters the battlefield tapped and adds one green mana to your mana pool. You may tap Sanctum of Verdant Growth and pay 3 mana to search your library for a basic Forest card and put it onto the battlefield tapped."
        self.image_path:str="cards/land/Sanctum of Verdant Growth/image.jpg"

    def generate_mana(self) -> dict:
        return {"G":1}

    @select_object("", 1)
    async def when_enter_landarea(
        self,
        player: "Player" = None,
        opponent: "Player" = None,
        selected_object: tuple = (),
        **kwargs,
    ):
        self.tap()
        player.mana["G"] += 1
        player.action_store.add_action(actions.Change_Mana(self, player, player.get_manas()))


    async def when_clicked(self, player: "Player" = None, opponent: "Player" = None,manual:bool=False):
        if self not in player.land_area:
            return False
        if self.get_flag("tap"):
            return False

        self.player.add_counter_dict("spend_land_count",1)
        self.tap()

        forests = player.get_cards_by_pos_type("library",(Forest,))
        check_result=self.player.check_can_use({"colorless":3,"U":0,"W":0,"B":0,"R":0,"G":0},except_land=[self])
        if not manual or not check_result[0] or not forests:
            
            mana=self.generate_mana()
            for key in mana:
                player.mana[key]+=mana[key]
            return True
        else:
            await self.player.generate_and_consume_mana(check_result[1],{"colorless":3,"U":0,"W":0,"B":0,"R":0,"G":0},self)
            
            picked = random.choice(forests)
            player.remove_card(picked, "library")
            player.append_card(picked, "land_area")
            picked.tap()
            return True


