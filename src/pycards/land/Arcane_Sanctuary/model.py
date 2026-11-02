
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.land import Land
from game.type_action import actions
from game.game_function_tool import select_object

class Arcane_Sanctuary(Land):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"draw_count":1,"scry_count":2,"mana_amount":1,"activation_cost":2}

        self.fixed_id:int=165

        self.name:str="Arcane Sanctuary"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="black"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Arcane Sanctuary enters the battlefield tapped and adds {mana_amount_word} colorless mana to your mana pool. You may also tap Arcane Sanctuary and pay {activation_cost} mana to scry {scry_count} and draw {draw_count_article} card{draw_count_plural}."
        self.image_path:str="cards/land/Arcane Sanctuary/image.jpg"

    def generate_mana(self) -> dict:
        return {"colorless":self.effect_params["mana_amount"]}

    @select_object("",1)
    async def when_enter_landarea(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        self.tap()
        player.mana["colorless"]+=self.effect_params["mana_amount"]
        player.action_store.add_action(actions.Change_Mana(self, player, player.get_manas()))



    async def when_clicked(self, player: "Player" = None, opponent: "Player" = None,manual:bool=False):
        # Mana abilities only apply while the land is in its owner's land zone (not e.g. mis-zoned on battlefield).
        if self not in self.player.land_area:
            return False
        if not self.get_flag("tap"):
            self.player.add_counter_dict("spend_land_count",1)
            check_result=self.player.check_can_use({"colorless":self.effect_params["activation_cost"],"U":0,"W":0,"B":0,"R":0,"G":0},except_land=[self])
            if not manual or not check_result[0]:
                mana=self.generate_mana()
                for key in mana:
                    player.mana[key]+=mana[key]
                self.tap()
            else:
                await self.player.generate_and_consume_mana(check_result[1],{"colorless":self.effect_params["activation_cost"],"U":0,"W":0,"B":0,"R":0,"G":0},self)
                await self.Scry(player, opponent, self.effect_params["scry_count"])
                player.draw_card(self.effect_params["draw_count"])
                self.tap()
                
                

            #self.flag_dict["tap"]=True#横置
            return True
        else:
            return False
