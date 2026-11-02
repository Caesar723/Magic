
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.land import Land
from game.type_action import actions
from game.game_function_tool import select_object


class Arcane_Haven(Land):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"mana_amount":1,"life_threshold":10}

        self.fixed_id:int=164

        self.name:str="Arcane Haven"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="colorless"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Arcane Haven enters the battlefield untapped and adds {mana_amount_word} colorless mana to your mana pool. You may also tap Arcane Haven to add one mana of any color to your mana pool if your's life above {life_threshold}."
        self.image_path:str="cards/land/Arcane Haven/image.jpg"

    @select_object("",1)
    async def when_enter_landarea(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        self.tap()
        player.mana["colorless"]+=self.effect_params["mana_amount"]
        player.action_store.add_action(actions.Change_Mana(self, player, player.get_manas()))

    def generate_mana(self) -> dict:
        if self.player.life>self.effect_params["life_threshold"]:
            return {"colorless":self.effect_params["mana_amount"]}
        else:
            return {}

    def check_ability_can_be_used(self,player:'Player'=None,opponent:'Player'=None):
        return (player or self.player).life>self.effect_params["life_threshold"]
