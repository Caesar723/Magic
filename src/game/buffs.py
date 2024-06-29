from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.card import Card
    from game.type_cards.creature import Creature


import types




#setattr(instance, 方法名, property(new_func))如果是state要property的用property(new_func)，否则就直接用new_func
class Buff:
    
    def __init__(self,card:"Card") -> None:
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str=""#这个buff是用在那个类型的
        self.content:str=""#描述buff

    def change_function(self,card:"Card"):
        pass

class StateBuff(Buff):
    def __init__(self,card:"Card",power:int,live:int) -> None:
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str="State"#这个buff是用在那个类型的
        unit=lambda num:"-" if num<0 else "+"
        self.content:str=f"{unit(power)}{power}/{unit(live)}{live}"#描述buff
        self.power=power
        self.live=live

    def change_function(self,card:"Creature"):
        previews_func=card.calculate_state
        def calculate_state(self_card):
            power,live=previews_func()
            power+=self.power
            live+=self.live
            return (power,live)
        card.calculate_state = types.MethodType(calculate_state, card)