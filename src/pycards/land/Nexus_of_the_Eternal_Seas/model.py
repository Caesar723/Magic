
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.land import Land
from game.type_action import actions
from game.game_function_tool import select_object
import random

class Nexus_of_the_Eternal_Seas(Land):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=173

        self.name:str="Nexus of the Eternal Seas"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="blue"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Nexus of the Eternal Seas enters the battlefield tapped and adds one blue mana to your mana pool. You may tap Nexus of the Eternal Seas to return random opponent's creature to its owner's hand."
        self.image_path:str="cards/land/Nexus of the Eternal Seas/image.jpg"

    def generate_mana(self) -> dict:
        return {"U":1}

    @select_object("",1)
    async def when_enter_landarea(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        self.tap()
        player.mana["U"]+=1
        player.action_store.add_action(actions.Change_Mana(self, player, player.get_manas()))

    
    async def when_clicked(self, player: "Player" = None, opponent: "Player" = None,manual:bool=False):
        if self not in player.land_area:
            return False
        if self.get_flag("tap"):
            return False
        self.player.add_counter_dict("spend_land_count",1)
        self.tap()
        if not manual or not opponent.battlefield:
            
            mana=self.generate_mana()
            for key in mana:
                player.mana[key]+=mana[key]
            return True
        else:
            target = random.choice(opponent.battlefield)
            target.player.remove_card(target, "battlefield")
            target.player.append_card(type(target)(target.player), "hand")
            return True
