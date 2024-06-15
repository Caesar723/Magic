from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player


import re


from game.game_function_tool import validate_all_methods
from game.type_action import actions

import game.custom_print


class Card:

    def __init__(self,player) -> None:
        self.player:"Player"=player
        self.name:str=""
        self.flag_dict:dict={}
        #self.keyword_list:list=[]
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
    def cost(self)->dict[int]:# colorless,red, green, blue,black,white
        return self.calculate_cost()
    
    def calculate_cost(self)->dict[int]:# colorless,red, green, blue,black,white
        number_part=""
        
        color_dict={
            "colorless":0,
            "U":0,
            "W":0,
            "B":0,
            "R":0,
            "G":0
        }
        for word in self.mana_cost:
            if word.isdigit():
                number_part+=word
            else:
                color_dict[word]+=1
        if number_part:
            color_dict["colorless"]=int(number_part)
        return color_dict

    def check_can_use(self,player:'Player')->tuple[bool]:# check whether user can use this card , bool and reason
        player_mana=dict(self.player.mana)
        cost=self.cost
        difference={key:cost[key]-player_mana[key] for key in player_mana}
        sum_negative_numbers = sum(difference[key] for key in difference if (difference[key] < 0 and key!='colorless'))
        difference["colorless"]+=sum_negative_numbers
        print(player_mana,cost,difference)
        land_store=[]

        for land in player.land_area:
            if land.check_can_use(player)[0]:
                mana=land.generate_mana()
                print(mana)
                for key in mana:
                    if difference[key]>0:
                        difference[key]-=mana[key]
                        land_store.append(land)
                    elif difference["colorless"]>0:
                        difference["colorless"]-=mana[key]
                        land_store.append(land)
        print(difference)
        all_values_less_than_zero = all(value <= 0 for value in difference.values())
        if all_values_less_than_zero:
            return (True,land_store)#第二个list是如果用[。。。]这些就可以打出这个牌
        else:
            return (False,"not enough cost")


       
        

    

    def attact_to_object(self,object):# it won't get hurt object can be card ot player
        self.player.action_store.add_action(actions.Attack_To_Object(self,self.player,object))

    def cure_to_object(self,object):# it won't get hurt
        self.player.action_store.add_action(actions.Cure_To_Object(self,self.player,object))
    
    async def selection_step(self, player: "Player" = None, opponent: "Player" = None)->list:# 当打出牌是，会调用此函数，给用户发送卡牌选项,返回项必须是数组
        return []
    async def when_play_this_card(self,player:'Player'=None,opponent:'Player'=None):# when player use the card return prepared function
        pass
        
    async def when_use_this_card(self,player:'Player',opponent:'Player'):# 先use check cost再play
        # checked_result=self.check_can_use(player)
        # if not checked_result[0]:
        #     return checked_result
        # else:
        self.player.action_store.start_record()
        
    
        prepared_function=await self.when_play_this_card(player,opponent)
        if prepared_function!="cancel":
            self.player.action_store.add_action(actions.Play_Cards(self,self.player))
        self.player.action_store.end_record()
        return (True,prepared_function)
    
        
            

    # def when_enter_battlefield(self):# 可以检查时候要用when_play_this_card如果是打出的可以用，如果是召唤的不用
    #     用在creature

    def when_go_to_hand(self):#当卡牌进入手牌
        pass

    def when_go_to_library(self):#当卡牌进入牌库
        pass

    def when_discard(self):#当卡牌被弃置
        pass

    def get_flag(self,flag_name:str)->bool:
        if flag_name in self.flag_dict:
            return self.flag_dict[flag_name]
        else:
            return False

    # def check_keyword(self,keyword:str)->bool:#检查关键词条,比如检查是否有吸血，key是吸血
    #     if keyword in self.keyword_list:
    #         return True
    #     return False
    
    # def add_keyword(self,keyword:str)->bool:#检查关键词条,比如检查是否有吸血，key是吸血
    #     if not (keyword in self.keyword_list):
    #         return True
    #     return False
    
    # def remove_keyword(self,keyword:str)->bool:#检查关键词条,比如检查是否有吸血，key是吸血
    #     if keyword in self.keyword_list:
    #         return True
    #     return False

    def when_a_creature_die(self,creature):#当随从死亡时（放入一个死亡随从的参数）
        pass

    def when_an_object_hert(self,object):#当一个card or 人物收到伤害，object是card 或者 player
        pass

    def create_selection(self,content:str,index:int):#生成一个selection，图片和名字是一样的，但是type_card和content是选项内容
        _class=type(self)
        new_selection=_class(self.player)
        new_selection.content=content
        new_selection.type_card=f"Selection {index}"
        new_selection.selection_index=index
        return new_selection

    
    def text(self,player:'Player',show_hide:bool=False)-> str:
        pass



if __name__=="__main__":
    card=Card("123")
    print(card.cost)