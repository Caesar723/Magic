
from __future__ import annotations
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.buffs import Tap


class Ironclad_Crusader(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Ironclad Crusader"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Human Knight"
        self.type:str="Creature"

        self.mana_cost:str="1WW"
        self.color:str="gold"
        self.type_card:str="Human Knight"
        self.rarity:str="Common"
        self.content:str="When Ironclad Crusader enters the battlefield, you may tap target creature an opponent controls. That creature doesn't untap during its controller's next untap step."
        self.image_path:str="cards/creature/Ironclad Crusader/image.jpg"



    @select_object("opponent_creatures", 1)
    async def when_enter_battlefield(self,player:Player,opponent:Player,selected_object:tuple['Card']=()) -> None:
        """Trigger ability when Ironclad Crusader enters the battlefield.
        Tap target creature an opponent controls. That creature doesn't untap during its controller's next untap step."""
        if selected_object:
            buff=Tap(self,selected_object[0])
            selected_object[0].gain_buff(buff,self)
            