from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.card import Card
    from game.type_cards.creature import Creature


import types




#setattr(instance, 方法名, property(new_func))如果是state要property的用property(new_func)，否则就直接用new_func
class Buff:
    
    def __init__(self,card:"Card",selected_card:"Card") -> None:
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str=""#这个buff是用在那个类型的
        self.content:str=""#描述buff
        self.buff_missile="Missile_Hit"
        self.color_missile="rgba(203, 203, 203, 0.9)"
        self.buff_name="Buff"
        self.selected_card=selected_card
        
        

    def change_function(self,card:"Card"):
        pass
    
    def set_end_of_turn(self):
        
        self.selected_card.player.put_card_to_dict("end_step_buff",self)

    def when_end_turn(self):
        self.selected_card.loss_buff(self,self.card)
        
        self.selected_card.player.remove_card_from_dict("end_step_buff",self)

    def text(self,player):
        image_link=self.card.image_path
        content=self.content
        Id=id(self)
        Id_card=id(self.selected_card)
        return f"Buff(string({self.buff_name}),string({image_link}),string({content}),int({Id}),int({Id_card}))"


class StateBuff(Buff):
    def __init__(self,card:"Card",selected_card:"Card",power:int,live:int) -> None:
        super().__init__(card,selected_card)
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str="State"#这个buff是用在那个类型的
        unit=lambda num:"-" if num<0 else "+"
        self.content:str=f"{unit(power)}{power}/{unit(live)}{live}"#描述buff
        self.power=power
        self.live=live
        self.buff_name=f"{card.name}"

    def change_function(self,card:"Creature"):
        previews_func=card.calculate_state
        def calculate_state(self_card):
            power,live=previews_func()
            power+=self.power
            live+=self.live
            return (power,live)
        card.calculate_state = types.MethodType(calculate_state, card)

class KeyBuff(Buff):
    def __init__(self,card:"Card",selected_card:"Card",key_name:str) -> None:
        super().__init__(card,selected_card)
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str="Key"#这个buff是用在那个类型的
        
        self.content:str=f"{key_name}"#描述buff
        self.key_name=key_name
        self.buff_name=f"{card.name}"
    def change_function(self,card:"Creature"):
        previews_func=card.get_flag
        def get_flag(self_card,key):
            result=previews_func(key)
            if key==self.key_name:
                return True
            return result
        card.get_flag = types.MethodType(get_flag, card)

class Frozen(Buff):
    def __init__(self,card:"Card",selected_card:"Card") -> None:
        super().__init__(card,selected_card)
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str="Frozen"#这个buff是用在那个类型的
        self.content:str="frozen"#描述buff
        self.buff_name=f"{card.name}"
        self.set_end_of_turn()

    def change_function(self,card:"Creature"):
        previews_func=card.get_flag
        def get_flag(self_card,key):
            result=previews_func(key)
            if key=="tap":
                return True
            
            return result
        card.get_flag = types.MethodType(get_flag, card)
    
class Tap(Frozen):
    def __init__(self,card:"Card",selected_card:"Card") -> None:
        super().__init__(card,selected_card)
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str="Tap"#这个buff是用在那个类型的
        self.content:str="tap"#描述buff
        self.buff_name=f"{card.name}"
        self.set_end_of_turn()

    def change_function(self,card:"Creature"):
        previews_func=card.get_flag
        card.tap()
        def get_flag(self_card,key):
            result=previews_func(key)
            if key=="tap":
                return True
            
            return result
        
        def untap(self_card):
            pass
        card.get_flag = types.MethodType(get_flag, card)
        card.untap = types.MethodType(untap, card)
    def when_end_turn(self):
        super().when_end_turn()
        self.selected_card.untap()


class Indestructible(Buff):
    def __init__(self,card:"Card",selected_card:"Card") -> None:
        super().__init__(card,selected_card)
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str="State"#这个buff是用在那个类型的
        self.content:str="indestructible"#描述buff
        self.buff_name=f"{card.name}"

    def change_function(self,card:"Creature"):
        previews_func_flag=card.get_flag
        previews_func_take_damage=card.take_damage
        async def take_damage(self_card,card,value,player, opponent):# 可以受到来自各种卡牌的伤害
            power,live=self_card.state
            if live-value<=0:
                value=live-1
            result=previews_func_take_damage(card,value,player,opponent)
            return result

        def get_flag(self_card,key):
            result=previews_func_flag(key)
            if key=="die":
                return False
            return result
        
        def die(self_card):
            pass
        card.get_flag = types.MethodType(get_flag, card)
        card.take_damage = types.MethodType(take_damage, card)
        card.die = types.MethodType(die, card)