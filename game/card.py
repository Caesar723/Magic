from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player



from game.game_function_tool import validate_all_methods
from game.type_action import actions



class Card:

    def __init__(self) -> None:
        self.name:str=""
        self.keyword_list:list=[]
        self.type:str
        self.current_position:str=""#library,battlefield,land_area,hand

        #card detail for js
        self.mana_cost:str
        self.color:str
        self.type_card:str
        self.rarity:str
        self.content:str
        self.image_path:str

    @property
    def cost(self)->list[int]:# colorless,red, green, blue,black,white
        return 

    def check_can_use(self,player:'Player')->tuple[bool, str]:# check whether user can use this card , bool and reason
        pass

    def attact_to_object(self,object):# it won't get hurt object can be card ot player
        pass

    def cure_to_object(self,object):# it won't get hurt
        pass
    
    def when_play_this_card(self,player:'Player'=None,opponent:'Player'=None):# when player use the card
        pass
        
    def when_use_this_card(self,player:'Player',opponent:'Player'):# 先use check cost再play
        checked_result=self.check_can_use(player)
        if not checked_result[0]:
            return checked_result
        else:
            self.when_play_this_card(player,opponent)
            return (True,'')
        
            

    # def when_enter_battlefield(self):# 可以检查时候要用when_play_this_card如果是打出的可以用，如果是召唤的不用
    #     用在creature

    def when_go_to_hand(self):#当卡牌进入手牌
        pass

    def when_go_to_library(self):#当卡牌进入牌库
        pass

    def when_discard(self):#当卡牌被弃置
        pass

    def check_keyword(self,keyword:str):#检查关键词条,比如检查是否有吸血，key是吸血
        pass

    def when_a_creature_die(self,creature):#当随从死亡时（放入一个死亡随从的参数）
        pass

    def when_an_object_hert(self,object):#当一个card or 人物收到伤害，object是card 或者 player
        pass
    



if __name__=="__main__":
    card=Card("123")
    print(card.cost)