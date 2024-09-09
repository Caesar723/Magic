
from __future__ import annotations
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.buffs import Tap


class Radiant_Angel_Buff(Tap):
    def __init__(self,card:"Card",selected_card:"Card") -> None:
        super().__init__(card,selected_card)
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str="Radiant_Angel"#这个buff是用在那个类型的
        self.content:str="unable to attack or block this turn"#描述buff
        self.buff_name=f"{card.name}"
    
class Radiant_Angel(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Radiant Angel"
        self.live:int=4
        self.power:int=4
        self.actual_live:int=4
        self.actual_power:int=4

        self.type_creature:str="Creature - Angel"
        self.type:str="Creature"

        self.mana_cost:str="3WW"
        self.color:str="gold"
        self.type_card:str="Creature - Angel"
        self.rarity:str="Rare"
        self.content:str="Flying, Lifelink. Whenever Radiant Angel deals damage, it illuminates all creatures with dark attributes, making them unable to attack or block this turn."
        self.image_path:str="cards/creature/Radiant Angel/image.jpg"

        self.flag_dict['lifelink']=True
        self.flag_dict['flying']=True

    async def when_harm_is_done(self,card:"Creature|Player",value:int,player: "Player" = None, opponent: "Player" = None):#当造成伤害时 OK
        result= await super().when_harm_is_done(card,value,player,opponent)
        for battle in [player.battlefield,opponent.battlefield]:    
            for creature_self in battle:
                if creature_self.color=="black":
                    buff=Radiant_Angel_Buff(self,creature_self)
                    creature_self.gain_buff(buff,self)
        return result