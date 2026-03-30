
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.land import Land
from game.type_action import actions
from game.game_function_tool import select_object

class Mystic_Reflection_Pool(Land):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=172

        self.name:str="Mystic Reflection Pool"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="blue"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Mystic Reflection Pool enters the battlefield untapped and adds one blue mana to your mana pool. Additionally, you may tap Mystic Reflection Pool and pay 1 mana to scry 2, then draw a card."
        self.image_path:str="cards/land/Mystic Reflection Pool/image.jpg"

    def generate_mana(self) -> dict:
        return {"U":1}

    @select_object("",1)
    async def when_enter_landarea(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        self.tap()
        player.mana["U"]+=1
        player.action_store.add_action(actions.Change_Mana(self, player, player.get_manas()))



    async def when_clicked(self, player: "Player" = None, opponent: "Player" = None,manual:bool=False):
        # Mana abilities only apply while the land is in its owner's land zone (not e.g. mis-zoned on battlefield).
        if self not in self.player.land_area:
            return False
        if not self.get_flag("tap"):
            self.player.add_counter_dict("spend_land_count",1)
            check_result=self.player.check_can_use({"colorless":1,"U":0,"W":0,"B":0,"R":0,"G":0},except_land=[self])
            if not manual or not check_result[0]:
                mana=self.generate_mana()
                for key in mana:
                    player.mana[key]+=mana[key]
                self.tap()
            else:
                await self.player.generate_and_consume_mana(check_result[1],{"colorless":2,"U":0,"W":0,"B":0,"R":0,"G":0},self)
                await self.Scry(player, opponent, 2)
                player.draw_card(1)
                self.tap()
                

            #self.flag_dict["tap"]=True#横置
            return True
        else:
            return False
