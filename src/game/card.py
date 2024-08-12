from typing import TYPE_CHECKING,Union
if TYPE_CHECKING:
    from game.player import Player
    from game.type_cards.creature import Creature


import re
import random
import inspect

from game.game_function_tool import validate_all_methods,reset_instance_methods
from game.type_action import actions
from game.buffs import Buff
import game.custom_print


class Card:

    def __init__(self,player) -> None:
        self.player:"Player"=player
        self.name:str=""
        self.flag_dict:dict={}
        """
        reach
        Trample
        flying
        haste
        summoning_sickness
        Flash
        lifelink
        """

        self.buffs:list[Buff]=[]
        #counter dict like number of turns, number of cards used
        self.counter_dict:dict={}
        
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

        self.selection_index:int

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
        print(player.land_area)
        for land in player.land_area:
            if not land.get_flag("tap"):
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


    
    async def when_harm_is_done(self,card:Union["Creature","Player"],value:int,player: "Player" = None, opponent: "Player" = None):#当造成伤害时 OK
        if self.get_flag("lifelink"):
            await self.cure_to_object(self.player,value,"rgba(0, 200, 0, 0.9)","Missile_Hit")
        return value
        

    

    async def attact_to_object(self,object:Union["Creature","Player"],power:int,color:str,type_missile:str):# it won't get hurt object can be card ot player
        if isinstance(object,type(self.player)):
            object.take_damage(self,power)
            self.player.action_store.add_action(actions.Attack_To_Object(self,self.player,object,color,type_missile,[object.life]))
            await object.check_dead()
        else:
            object.take_damage(self,power,object.player,object.player.opponent) 
            self.player.action_store.add_action(actions.Attack_To_Object(self,self.player,object,color,type_missile,object.state))
            if await object.check_dead():
                self.when_kill_creature(object,self.player,self.player.opponent)

        await self.when_harm_is_done(object,power,self.player,self.player.opponent)
        
        

    async def cure_to_object(self,object:Union["Creature","Player"],power:int,color:str,type_missile:str):# it won't get hurt
        if isinstance(object,type(self.player)):
            object.gains_life(self,power)
            self.player.action_store.add_action(actions.Cure_To_Object(self,self.player,object,color,type_missile,[object.life]))
            await object.check_dead()
        else:
            object.gains_life(self,power,object.player,object.player.opponent) 
            self.player.action_store.add_action(actions.Cure_To_Object(self,self.player,object,color,type_missile,object.state))
            if await object.check_dead():
                self.when_kill_creature(object,self.player,self.player.opponent)
    
    async def selection_step(self, player: "Player" = None, opponent: "Player" = None,selection_random:bool=False)->list:# 当打出牌是，会调用此函数，给用户发送卡牌选项,返回项必须是数组
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
    def when_go_to_battlefield(self, player: "Player" = None, opponent: "Player" = None):#这个是每次进入场地的时候
        pass
    def when_go_to_landarea(self, player: "Player" = None, opponent: "Player" = None):
        pass
    def when_go_to_hand(self):#当卡牌进入手牌
        pass

    def when_go_to_library(self):#当卡牌进入牌库
        pass

    async def when_discard(self,player: "Player" = None, opponent: "Player" = None):#当卡牌被弃置
        pass

    def get_flag(self,flag_name:str)->bool:
        if flag_name in self.flag_dict:
            return self.flag_dict[flag_name]
        else:
            return False

    def add_counter_dict(self,key:str,number:int)->None:# change the numebr of counter_dict
        if key in self.counter_dict:
            self.counter_dict[key]+=number
        else:
            self.counter_dict[key]=number
    def set_counter_dict(self,key:str,number:int)->None:# change the numebr of counter_dict
        
        self.counter_dict[key]=number
        
    def get_counter_from_dict(self,key:str):
        if key in self.counter_dict:
            return self.counter_dict[key]
        else:
            return 0
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

    def when_a_creature_die(self,creature:"Creature",player: "Player" = None, opponent: "Player" = None):#当随从死亡时（放入一个死亡随从的参数）
        pass

    def when_an_object_hert(self,object,player: "Player" = None, opponent: "Player" = None):#当一个card or 人物收到伤害，object是card 或者 player
        pass

    def when_kill_creature(self,card:"Creature",player: "Player" = None, opponent: "Player" = None):#OK
        pass

    def when_start_turn(self,player: "Player" = None, opponent: "Player" = None):#OK
        pass

    def when_end_turn(self,player: "Player" = None, opponent: "Player" = None):#OK
        pass

    def aura(self,player: "Player" = None, opponent: "Player" = None):
        pass

    def create_selection(self,content:str,index:int):#生成一个selection，图片和名字是一样的，但是type_card和content是选项内容
        _class=type(self)
        new_selection=_class(self.player)
        new_selection.content=content
        new_selection.type_card=f"Selection {index}"
        new_selection.selection_index=index
        return new_selection
    
    async def Scry(self,player:'Player',opponent:'Player',times:int):
        length_library=len(player.library)
        if times>length_library:
            cards=player.library[0:length_library]
        else:
            cards=player.library[0:times]

        selection_end=self.create_selection("End Selection",1)
        while cards:
            card=await player.send_selection_cards(cards+[selection_end])
            if card=="cancel":
                await player.send_text("end_select()")
                return
            elif card.content=="End Selection":
                return 
            else:
                player.remove_card(card,'library')
                player.append_card(card,'library')
                cards.remove(card)

    def check_overwritten(self,player:"Player"):#检查card的一些特殊函数有没有重写，如果重写了就放进dictionary
        func_dict={#这里要和player的initinal_card_dict一致
            "end_step":(Card.when_end_turn,self.when_end_turn),
            "upkeep_step":(Card.when_start_turn,self.when_start_turn),
            "when_creature_die":(Card.when_a_creature_die,self.when_end_turn),
            "aura":(Card.aura,self.aura),
        }
        for key in func_dict:
            if inspect.getsource(func_dict[key][0]) != inspect.getsource(func_dict[key][1]):
                player.put_card_to_dict(key,self)
        #inspect.getsource(Card.my_method) != inspect.getsource(Child.my_method):


    def when_gain_buff(self,player: "Player" = None, opponent: "Player" = None,buff:Buff=None,card:'Card'=None):#当获得+1+1的buff时 OK
        self.player.action_store.start_record()
        
    
        
        self.player.action_store.add_action(actions.Add_Buff(card,card.player,self,"rgba(236, 230, 233, 0.8)","None",(),buff,True))
        self.player.action_store.end_record()

    def when_loss_buff(self,player: "Player" = None, opponent: "Player" = None,buff:Buff=None,card:'Card'=None):#当失去+1+1的buff时 OK
        self.player.action_store.start_record()

        self.player.action_store.add_action(actions.Lose_Buff(card,card.player,self,(),buff,True))
        self.player.action_store.end_record()

    def loss_buff(self,buff,card):#card 是给这个牌buff的牌
        if buff in self.buffs:
            self.buffs.remove(buff)
            self.update_buff()
            self.when_loss_buff(self.player,self.player.opponent,buff,card)
        else:
            self.update_buff()
        

    def gain_buff(self,buff,card):
        self.buffs.append(buff)
        self.update_buff()
        self.when_gain_buff(self.player,self.player.opponent,buff,card)

    def update_buff(self):
        reset_instance_methods(self)
        self.change_function_by_buff()
        
    def change_function_by_buff(self):#遍历buffs，改变函数
        for buff in self.buffs:
            buff.change_function(self)
            
    
    def text(self,player:'Player',show_hide:bool=False)-> str:
        pass



if __name__=="__main__":
    card=Card("123")
    print(card.cost)