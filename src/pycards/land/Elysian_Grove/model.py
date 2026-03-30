
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.land import Land
from game.game_function_tool import select_object
from game.type_action import actions
import random
from game.buffs import Tap

class Elysian_Grove(Land):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=167

        self.name:str="Elysian Grove"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="green"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Elysian Grove enters the battlefield tapped and adds one green mana to your mana pool. You may tap Elysian Grove to tap random opponent's land."
        self.image_path:str="cards/land/Elysian Grove/image.jpg"

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
        if not manual or not opponent.land_area:
            self.player.add_counter_dict("spend_land_count",1)
            mana=self.generate_mana()
            for key in mana:
                player.mana[key]+=mana[key]
            self.tap()
            return True
        else:
            target = random.choice(opponent.land_area)
            
            buff=Tap(self,target)
            target.gain_buff(buff,self)
            self.tap()
            return True
