
if __name__=="__main__":
    import sys
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/")

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fastapi import WebSocket
    from game.room import Room
import random
import asyncio


#from game.action import Action
from game.type_action import actions
from game.card import Card
from initinal_file import CARD_DICTION
from game.type_cards.creature import Creature
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery
from game.type_cards.instant import Instant

from starlette.websockets import WebSocketDisconnect
import game.custom_print

  

class Player:

    

    def __init__(self,name:str,decks_detail:str,room:"Room") -> None:
        self.name=name
        self.room=room

        self.opponent:Player#opponent player

        #the life of player
        self.ini_life:int=20
        self.life:int=20

        #list of Graveyard 墓地 这里可以包含所有的卡牌而不只是随从
        self.graveyard:list[Card]=[]

        #list of Library牌库
        self.library:list[Card]=[]

        #list of Battlefield 场地
        self.battlefield:list[Creature]=[]

        #land area
        self.land_area:list[Land]=[]

        #hand area
        self.hand:list[Card]=[]

        #exile area
        self.exile_area:list[Card]=[]

        #mana cost [colorless, blue,white,black,red,green]
        self.mana={"colorless":0,"U":0,"W":0,"B":0,"R":0,"G":0}

        #counter dict like number of turns, number of cards used
        self.counter_dict:dict={}
        self.counter_dict["lands_summon_max"]=1

        #flag dict like whethr is your tern, whether ....
        self.flag_dict:dict={}

        #cards_store_dict each element store list of cards
        '''
        cards_store_dict可以拿来存放一些特殊效果卡牌,
        比如具有当回合开始时效果的卡牌，
        让回合开始时，它可以便利一遍里面的内容然后调用函数
        '''
        self.cards_store_dict:dict[list]={}

        #Aura光环 pool
        self.aura_pool:list[Card]=[]


        #action store
        self.action_store:actions.List_Action_Processor=room.action_processor

        #state of player Beginning Phase,In-Game State,Ending Phase
        self.state_of_gaming:str=""

        #attacker
        #self.attacker:Card=None

        #defenders
        #self.defenders:list[Card]=None

        self.future_function:asyncio.Task=""#done(): 判断 Future 是否已经完成（无论是正常完成还是抛出异常）。

        

        #游戏还没有开始
        self.deck:list[Card]=[]
        self.deck_detail:str=decks_detail
        

        #the socket used to select object
        self.socket_select_object:"WebSocket"
        #用于锁，确保每一次只想client发一个请求
        self.selection_lock = asyncio.Lock()
        self.socket_connected_flag=False
        self.selection_event=asyncio.Event()
    
    def set_opponent_player(self,opponent:"Player",room:'Room'):
        self.opponent:"Player"=opponent
        self.room:'Room'=room
        self.initinal_decks(self.deck_detail)
        self.initinal_card_dict()


    def set_socket(self,socket):
        pass

    def send_message(self,type:str,content:str):# the type of content and content
        pass

    def initinal_decks(self,decks_detail:str):#generate cards
        for element in decks_detail.split("|"):
            name,type,number=element.split("+")
            number=int(number)
            self.deck+=[CARD_DICTION[f"{name}_{type}"](self) for i in range(number)]
        random.shuffle(self.deck)
        self.hand=self.deck[:7]# get 7 card to hand
        self.library=self.deck[7:]# the rest is in the library

    def initinal_card_dict(self):# 回合开始，回合结束卡牌，光环。。。
        self.cards_store_dict["upkeep_step"]=[]
        self.cards_store_dict["end_step"]=[]
        self.cards_store_dict["aura"]=[]#光环，存具有光环效果的牌，每当用户发送信息的时候都会触发一下光环来检查光环也没有失效
        self.cards_store_dict["when_creature_die"]=[]
    def get_cards_from_dict(self,key:str)->list[Card]:
        if key in self.cards_store_dict:
            return self.cards_store_dict[key]
        else:
            return []
        
    def put_card_to_dict(self,key:str,card:Card)->None:# put a card to self.cards_store_dict
        if key in self.cards_store_dict:
            if card not in self.cards_store_dict[key]:
                self.cards_store_dict[key].append(card)
        else:
            self.cards_store_dict[key]=[card]
    
    def remove_card_from_dict(self,key:str,card:Card)->None:
        if key in self.cards_store_dict:
            if card in self.cards_store_dict[key]:
                self.cards_store_dict[key].remove(card)
            
        else:
            self.cards_store_dict[key]=[]



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
    def draw_card(self,number:int):# draw x cards from library
        self.action_store.start_record()
        for i in range(number):
            if not (self.library):
                self.flag_dict["die"]=True
                self.action_store.end_record()
                return 
            card=self.library[0]
            self.remove_card(card,'library')
            self.append_card(card,'hand')
        self.action_store.end_record()
            

    def gains_life(self,card:Card,value:int):
        
        self.life+=value
        if self.life>self.ini_life:
            self.life=self.ini_life
        self.when_gaining_life(card,value)

   
    def take_damage(self,card:Card,value:int)->int:
        value=max(value,0)
        self.life-=value
        self.when_dealt_damage(card,value)

    async def check_dead(self):
       if self.life<=0:
           self.flag_dict["die"]=True
           
       return self.get_flag("die")
    

    def select_attacker(self,card:Creature):# select_creature_as_attacker, the index of battlefield
        
        #card.when_become_attacker()
        return 

    def select_defender(self,card:Creature):# select_creature_as_defender
        #card.when_become_defender()
        return
    def deal_damage_player(self):# Deal damage to player
        pass

    def gain_life_player(self):# gain life to player
        pass

    def when_dealt_damage(self,card:"Card",value:int):#when players live decrease
        pass

    def when_gaining_life(self,card:"Card",value:int):#when players live increase
        pass

    

    async def play_a_card(self,card:Card):# player 打出一张牌
        checked_result=card.check_can_use(self)
        #print(checked_result)
        if checked_result[0]:
            self.action_store.start_record()#
            
            result=await card.when_use_this_card(self,self.opponent)
            #(result)
            if result[1]=="cancel":
                self.action_store.end_record()
                await self.send_text("end_select()")
                return (False,"Selection Error")
            
            for land in checked_result[1]:
                if not await land.when_clicked(self,self.opponent):
                    self.action_store.end_record()
                    return (False,"Can't use land")
            for card_when_play in self.get_cards_from_dict("when_play_a_card"):
                if card_when_play!=card:
                    await card_when_play.when_play_a_card(card,self,self.opponent)
            self.action_store.add_action(actions.Change_Mana(self,self,self.get_manas()))
            self.action_store.end_record()

            self.action_store.start_record()#
            self.mana_consumed(card.cost)
            self.action_store.add_action(actions.Change_Mana(card,self,self.get_manas()))
            self.action_store.end_record()
            
            
            
            
            #print(result)
            #result[1]()
            return result
        else:
            return checked_result
        
    
    async def check_creature_die(self,card:Creature):
        if card.get_flag("exile"):
            await card.when_move_to_exile_area(self,self.opponent)
            return True
        result=await card.check_dead()
        if result:
            #self.action_store.start_record()
            for card_self in self.get_cards_from_dict("when_creature_die"):
                if card_self!=card:
                    await card_self.when_a_creature_die(card,card_self.player,card_self.player.opponent)
            for card_opponent in self.opponent.get_cards_from_dict("when_creature_die"):
                if card_opponent!=card:
                    await card_opponent.when_a_creature_die(card,card_opponent.player,card_opponent.player.opponent)
            await card.when_move_to_graveyard(self,self.opponent)
            #self.action_store.end_record()
            # card.when_die(self,self.opponent)
            # card.when_leave_battlefield(self,self.opponent,'graveyard')
        return result
    

    async def beginning_phase(self):#开始阶段
        self.return_to_org_max_land()
        self.untap_step()
        await self.upkeep_step()
        self.draw_step()
       
    def return_to_org_max_land(self):#让lands_summon_max 变回1
        self.counter_dict["lands_summon_max"]=1
        self.counter_dict["lands_summon"]=0
        
    def untap_step(self):#解除操控步骤:土地被横置以产生法术力（Mana），生物被横置以攻击等
        for land in self.land_area:
            land.untap()
        for creature in self.battlefield:
            creature.untap()
            if creature.get_flag("Double strike"):
                creature.set_counter_dict("attack_counter",2)
            else:
                creature.set_counter_dict("attack_counter",1)

    async def upkeep_step(self):#保持步骤（Upkeep Step）：某些卡牌效果会在这个时候触发。
        for card in self.get_cards_from_dict("upkeep_step"):
            self.action_store.start_record()
            await card.when_start_turn(self,self.opponent)
            self.action_store.end_record()

    def draw_step(self):#抓牌步骤（Draw Step）通常情况下，玩家在这一步抓一张牌。
        self.draw_card(1)


    def inGame_state(self):# 切换到inGame_state
        pass

    async def ending_phase(self):#结束阶段 清空法术力（包括敌方）
        #self.action_store.start_record()
        self.end_step()
        await self.cleanup_step()
        #self.action_store.end_record()
        

    def end_step(self):#结束步骤（End Step）：某些卡牌效果会在这个时候触发。
        for creature in self.battlefield:
            creature.end_summoning_sickness()

        for card in self.get_cards_from_dict("end_step"):
            self.action_store.start_record()
            card.when_end_turn(self,self.opponent)
            self.action_store.end_record()
            
        self.action_store.start_record()
        for buff in list(self.get_cards_from_dict("end_step_buff")):
            buff.when_end_turn()
        self.action_store.end_record()

    async def cleanup_step(self):#清理步骤（Cleanup Step）：玩家将手牌调整至最大手牌限制，移除所有“直到回合结束”类的效果，并移除所有受到的伤害。清空法术力（包括敌方）
        self.mana={"colorless":0,"U":9,"W":9,"B":9,"R":9,"G":9}
        self.opponent.mana={"colorless":0,"U":9,"W":9,"B":9,"R":9,"G":9}
        self.action_store.add_action(actions.Change_Mana(self,self,self.get_manas()))
        self.opponent.action_store.add_action(actions.Change_Mana(self.opponent,self.opponent,self.opponent.get_manas()))

    def get_card_index(self,index:int,type:str):# get card by index,type:battlefield,hand,land_area
        deck_type={
            'battlefield':self.battlefield,
            'hand':self.hand,
            'land_area':self.land_area
        }
        
        if type in deck_type and index<len(deck_type[type]):
            return deck_type[type][index]
        else:
            return False

    def remove_card(self,card:Card,type:str):#会发送消息给client
        deck_type={
            'battlefield':self.battlefield,
            'hand':self.hand,
            'land_area':self.land_area,
            'graveyard':self.graveyard,
            'library':self.library,
            'exile_area':self.exile_area
        }
        if type in deck_type and card in deck_type[type]:
            keys=card.check_overwritten()
            for key in keys:
                self.remove_card_from_dict(key,card)
            deck_type[type].remove(card)
            if type=='hand':
                self.action_store.add_action(actions.Lose_Card(self,self,card,True))# 一定是需要的，这个动作
            elif  (type=='land_area' or type=='battlefield'):
                self.action_store.add_action(actions.Die(card,self))# 一定是需要的，这个动作
    

        

        


    def append_card(self,card:Card,type:str):#会发送消息给client
        deck_type={
            'battlefield':self.battlefield,
            'hand':self.hand,
            'land_area':self.land_area,
            'graveyard':self.graveyard,
            'library':self.library,
            'exile_area':self.exile_area
        }
        
        if type in deck_type:
            keys=card.check_overwritten()
            for key in keys:
                self.put_card_to_dict(key,card)
            deck_type[type].append(card)
        
            if type=='hand':
                self.action_store.add_action(actions.Gain_Card(self,self,card,True))
            elif type=='battlefield' :
                card.when_go_to_battlefield(card.player,card.player.opponent)
                self.action_store.add_action(actions.Summon(card,self))

            elif type=='land_area':
                card.when_go_to_landarea(card.player,card.player.opponent)
                self.action_store.add_action(actions.Summon(card,self))

    def mana_consumed(self,cost:"dict"):#自己的魔力池减少
        #cost=card.cost
        for key in cost:
            self.mana[key]-=cost[key]
        if self.mana["colorless"]<0:
            for key in self.mana:
                if key!="colorless":
                    while self.mana[key]>0 and self.mana["colorless"]<0:
                        self.mana[key]-=1
                        self.mana["colorless"]+=1
    def get_manas(self)->list:#[blue,white,black,red,green]
        result=[]
        for key in self.mana:
            if key!="colorless":
                result.append(self.mana[key])
        return result
    
    def discard(self,card:"Card"):
        if card in self.hand:
            self.remove_card(card,"hand")
            card.when_discard(self,self.opponent)


    async def send_selection_cards(self,selected_cards:list[Card],selection_random:bool=False):
        async with self.selection_lock:
            cards=','.join([card.text(self,False) for card in selected_cards])
            await self.send_text(f"select(cards,parameters({cards}))")
            data =await self.receive_text()# 玩家｜cards｜index
            selected_card=self.get_object(selected_cards,data)
        
        if selected_card=="cancel" and selection_random:
            if selected_cards:
                selected_card=random.choice(selected_cards)
            await self.send_text("end_select()")
        return selected_card
    
    def get_object(self,selected_cards:list[Card],data:str):
        parameters=data.split("|")
        room=self.room
        if parameters[1]=="cards" and room.players[parameters[0]]==self:
            index=int(parameters[2])
            if index<len(selected_cards):
                return selected_cards[index]
        elif parameters[1]=="cancel":
            return "cancel"

        


    # async def send_selection_players(self,card):
    #     async with self.selection_lock:
    #         pass

    async def receive_text(self):
        data=''
        try:
            data =await self.socket_select_object.receive_text()
            
        except WebSocketDisconnect as e:
            await self.socket_select_object.close()
            self.socket_select_object=None
            self.selection_event.set()
        return data
        
            

    async def send_text(self,message):
        try:
            await self.socket_select_object.send_text(message)
            
        except WebSocketDisconnect as e:
            await self.socket_select_object.close()
            self.socket_select_object=None
            self.selection_event.set()
        

    async def wait_selection_socket(self):
        await self.selection_event.wait()

    async def cancel_future_function(self):
        if (isinstance(self.future_function,asyncio.Task)) and (not self.future_function.done()):
            self.future_function.cancel()
            #await self.send_text("end_select()")

    def check_can_use(self,cost:dict)->tuple[bool]:#cost={"colorless":0,"U":0,"W":0,"B":0,"R":0,"G":0}
        player_mana=dict(self.mana)
        difference={key:cost[key]-player_mana[key] for key in player_mana}
        sum_negative_numbers = sum(difference[key] for key in difference if (difference[key] < 0 and key!='colorless'))
        difference["colorless"]+=sum_negative_numbers
        #print(player_mana,cost,difference)
        land_store=[]

        for land in self.land_area:
            if land.check_can_use(self)[0]:
                mana=land.generate_mana()
                #print(mana)
                for key in mana:
                    if difference[key]>0:
                        difference[key]-=mana[key]
                        land_store.append(land)
                    elif difference["colorless"]>0:
                        difference["colorless"]-=mana[key]
                        land_store.append(land)
        all_values_less_than_zero = all(value <= 0 for value in difference.values())
        if all_values_less_than_zero:
            return (True,land_store)#第二个list是如果用[。。。]这些就可以打出这个牌
        else:
            return (False,"not enough cost")
    
    async def generate_and_consume_mana(self,lands,cost,card:"Card"):#把generate mana 和consume mana 合并到一起
        self.action_store.start_record()#
        for land in lands:
            if not await land.when_clicked(self,self.opponent):
                return (False,"Can't use land")
        self.action_store.add_action(actions.Change_Mana(self,self,self.get_manas()))
        self.action_store.end_record()

        self.action_store.start_record()#
        self.mana_consumed(cost)
        self.action_store.add_action(actions.Change_Mana(card,self,self.get_manas()))
        self.action_store.end_record()
        

    def get_flag(self,flag_name:str):
        if flag_name in self.flag_dict:
            return self.flag_dict[flag_name]
        else:
            return False
        
    def get_cards_by_pos_type(self,position:str,card_type:tuple["Creature|Land|Sorcery|Instant"],except_type:tuple["Creature|Land|Sorcery|Instant"]=()):
        position_dict={
            'battlefield':self.battlefield,
            'hand':self.hand,
            'land_area':self.land_area,
            'graveyard':self.graveyard,
            'library':self.library,
            'exile_area':self.exile_area
        }
        
        if position in position_dict:
            #print(position_dict[position])
            cards=[card for card in position_dict[position] if  isinstance(card,card_type) and not isinstance(card,except_type)]
            return cards
        return []

        
    def text(self,player)-> str:
        if self.name==player.name:
            return f"player({self.name},Self)"
        else:
            return f"player({self.name},Opponent)"


    
if __name__=="__main__":

    
    
    player=Player("caesar","Mystic Tides+Instant+1|Mystic Reflection+Instant+1|Mystic Evasion+Instant+2|Mindful Manipulation+Sorcery+1|Nyxborn Serpent+Creature+1|Mistweaver Drake+Creature+1",[])
    print(player.deck)
    