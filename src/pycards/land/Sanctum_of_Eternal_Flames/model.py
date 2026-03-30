
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.land import Land
from game.type_action import actions
from game.game_function_tool import select_object
import random


class Sanctum_of_Eternal_Flames(Land):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=175

        self.name:str="Sanctum of Eternal Flames"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="red"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Sanctum of Eternal Flames enters the battlefield tapped and adds one red mana to your mana pool. You may also tap Sanctum of Eternal Flames and pay 2 mana to deal 2 damage to random opponent's creature or player."
        self.image_path:str="cards/land/Sanctum of Eternal Flames/image.jpg"

    def generate_mana(self) -> dict:
        return {"R":1}

    @select_object("",1)
    async def when_enter_landarea(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        self.tap()
        player.mana["R"]+=1
        player.action_store.add_action(actions.Change_Mana(self, player, player.get_manas()))

    
    async def when_clicked(self, player: "Player" = None, opponent: "Player" = None,manual:bool=False):
        if self not in player.land_area:
            return False
        if self.get_flag("tap"):
            return False
        self.player.add_counter_dict("spend_land_count",1)
        self.tap()

        check_result=self.player.check_can_use({"colorless":2,"U":0,"W":0,"B":0,"R":0,"G":0},except_land=[self])
        if not manual or not check_result[0]:
            
            mana=self.generate_mana()
            for key in mana:
                player.mana[key]+=mana[key]
            return True
        else:
            await self.player.generate_and_consume_mana(check_result[1],{"colorless":2,"U":0,"W":0,"B":0,"R":0,"G":0},self)
            choose_list=[*opponent.battlefield,opponent]
            target = random.choice(choose_list)
            await self.attact_to_object(target, 2, "rgba(255, 80, 0, 0.9)", "Missile_Hit")
            return True
       
