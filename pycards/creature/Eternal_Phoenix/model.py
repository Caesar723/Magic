
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Eternal_Phoenix(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Eternal Phoenix"
        self.live:int=3
        self.power:int=3
        self.actual_live:int=3
        self.actual_power:int=3

        self.type_creature:str="Phoenix Creature - Phoenix"
        self.type:str="Creature"

        self.mana_cost:str="2RR"
        self.color:str="red"
        self.type_card:str="Phoenix Creature - Phoenix"
        self.rarity:str="Rare"
        self.content:str="Flying, When Eternal Phoenix dies, if it didn't have a feather counter on it, return it to the battlefield with a feather counter on it instead of putting it into your graveyard."
        self.image_path:str="cards/creature/Eternal Phoenix/image.jpg"

        self.flag_dict["flying"]=True


    async def when_move_to_graveyard(self, player: "Player" = None, opponent: "Player" = None):#移入墓地 OK
        
        
        self.when_leave_battlefield(player,opponent,'graveyard')
        

        player.action_store.start_record()
        self.when_die(player,opponent)
        player.action_store.end_record()

        
        self.reset_to_orginal_state()

    def when_die(self,player: "Player" = None, opponent: "Player" = None):#OK
        if not self.get_flag("feather_Eternal_Phoenix"):
            new_creature=Eternal_Phoenix(player)
            player.append_card(new_creature,"battlefield")
            new_creature.flag_dict["feather_Eternal_Phoenix"]=True

        