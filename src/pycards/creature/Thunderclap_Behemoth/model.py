
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Thunderclap_Behemoth(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Thunderclap Behemoth"
        self.live:int=6
        self.power:int=6
        self.actual_live:int=6
        self.actual_power:int=6

        self.type_creature:str="Beast Creature - Beast"
        self.type:str="Creature"

        self.mana_cost:str="4GG"
        self.color:str="green"
        self.type_card:str="Beast Creature - Beast"
        self.rarity:str="Rare"
        self.content:str="Trample (This creature can deal excess combat damage to the player or planeswalker it's attacking.), Whenever Thunderclap Behemoth attacks, it deals 3 damage to each creature defending player controls if you control another creature with power 4 or greater."
        self.image_path:str="cards/creature/Thunderclap Behemoth/image.jpg"
        self.flag_dict["Trample"]=True

    async def when_start_attcak(self,defender:Creature,player:Player,opponent:Player):
        flag=False
        for creature in player.battlefield:
            if creature.state[0]>=4:
                flag=True
                break
        if flag:
            #for creature in opponent.battlefield:
            await self.attact_to_object(defender,3,"rgba(243, 243, 243, 0.9)","Missile_Hit")


        