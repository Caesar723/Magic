
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


class Verdant_Sanctuary(Land):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=178

        self.name:str="Verdant Sanctuary"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="green"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Verdant Sanctuary enters the battlefield tapped and adds one green mana to your mana pool. You may also tap Verdant Sanctuary and deal 3 damage to yourself to search your library for a basic Forest card and put it onto the battlefield tapped."
        self.image_path:str="cards/land/Verdant Sanctuary/image.jpg"

    def generate_mana(self) -> dict:
        return {"G":1}

    # tech_doc「Land-例子2」+ Creature.when_enter_battlefield：@select_object("",1) 包住函数体，
    # 打出地后堆叠结算时会执行函数体。文案中 “enters… and adds one green mana…” 的进场加费写在这里；
    # 横置再产费仍由 generate_mana + Land.when_clicked 处理。
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
        
        if not manual or player.life<3 or not forests:
            
            mana=self.generate_mana()
            for key in mana:
                player.mana[key]+=mana[key]
            return True
        else:
            await self.attact_to_object(player, 3, "rgba(0, 255, 0, 0.9)", "Missile_Hit")
            
            picked = random.choice(forests)
            player.remove_card(picked, "library")
            player.append_card(picked, "land_area")
            picked.tap()
            return True
