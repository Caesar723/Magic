
if __name__=="__main__":
    import sys
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/")

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fastapi import WebSocket
import random



from game.action import Action
from game.type_action import actions
from game.card import Card
from initinal_file import CARD_DICTION
from game.type_cards.creature import Creature
from game.type_cards.land import Land



  

class Player:

    

    def __init__(self,name:str,decks_detail:str,action_stroe:list[Action]) -> None:
        self.name=name

        self.opponent:Player#opponent player

        #the life of player
        self.ini_life:int=30
        self.life:int=30

        #list of Graveyard 墓地
        self.graveyard:list[Card]=[]

        #list of Library牌库
        self.library:list[Card]=[]

        #list of Battlefield 场地
        self.battlefield:list[Card]=[]

        #land area
        self.land_area:list[Card]=[]

        #hand area
        self.hand:list[Card]=[]

        #mana cost [colorless, blue,white,black,red,green]
        self.mana={"colorless":0,"U":0,"W":0,"B":0,"R":0,"G":0}

        #counter dict like number of turns, number of cards used
        self.counter_dict:dict={}

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
        self.action_store:list[Action]=action_stroe

        #state of player Beginning Phase,In-Game State,Ending Phase
        self.state_of_gaming:str=""

        #attacker
        #self.attacker:Card=None

        #defenders
        #self.defenders:list[Card]=None

        #the socket used to select object
        self.socket_select_object:"WebSocket"

        #游戏还没有开始
        self.deck:list[Card]=[]
        self.initinal_decks(decks_detail)
        self.initinal_card_dict()
    
    def set_opponent_player(self,opponent:"Player"):
        self.opponent:"Player"=opponent


    def set_socket(self,socket):
        pass

    def send_message(self,type:str,content:str):# the type of content and content
        pass

    def initinal_decks(self,decks_detail:str):#generate cards
        for element in decks_detail.split("|"):
            name,type,number=element.split("+")
            number=int(number)
            self.deck+=[CARD_DICTION[f"{name}_{type}"](self) for i in range(number)]
        #random.shuffle(self.deck)
        self.hand=self.deck[:7]# get 7 card to hand
        self.library=self.deck[7:]# the rest is in the library

    def initinal_card_dict(self):# 回合开始，回合结束卡牌，光环。。。
        self.cards_store_dict["upkeep_step"]=[]
        self.cards_store_dict["end_step"]=[]
        self.cards_store_dict["aura"]=[]
        
    def get_cards_from_dict(self,key:str):
        if key in self.cards_store_dict:
            return self.cards_store_dict[key]
        else:
            return []
        
    def put_card_to_dict(self,key:str,card:Card)->None:# put a card to self.cards_store_dict
        if key in self.cards_store_dict:
            self.cards_store_dict[key].append(card)
        else:
            self.cards_store_dict[key]=[]
    
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

    def draw_card(self,number:int):# draw x cards from library
        pass

    def change_live(self,change_of_live:int):
        pass

    

    def select_attacker(self,card:Creature):# select_creature_as_attacker, the index of battlefield
        
        card.when_become_attacker()

    def select_defender(self,card:Creature):# select_creature_as_defender
        card.when_become_defender()

    def deal_damage_player(self):# Deal damage to player
        pass

    def gain_life_player(self):# gain life to player
        pass

    def when_dealt_damage(self):#when players live decrease
        pass

    def when_gaining_life(self):#when players live increase
        pass

    async def play_a_card(self,card:Card):# player 打出一张牌
        checked_result=card.check_can_use(self)
        print(checked_result)
        if checked_result[0]:
            for land in checked_result[1]:
                if not land.when_clicked(self,self.opponent):
                    return (False,"Can't use land")
            self.mana_consumed(card)
            result=await card.when_use_this_card(self,self.opponent)
            print(result)
            #result[1]()
            return result
        else:
            return checked_result
    
    async def check_creature_die(self,card:Creature):
        result=await card.check_dead()
        if result:
            await card.when_move_to_graveyard(self,self.opponent)
            # card.when_die(self,self.opponent)
            # card.when_leave_battlefield(self,self.opponent,'graveyard')
        return result

    def beginning_phase(self):#开始阶段
        self.untap_step()
        self.upkeep_step()
        self.draw_step()

    def untap_step(self):#解除操控步骤:土地被横置以产生法术力（Mana），生物被横置以攻击等
        pass

    def upkeep_step(self):#保持步骤（Upkeep Step）：某些卡牌效果会在这个时候触发。
        for card in self.get_cards_from_dict("upkeep_step"):
            card.when_start_turn(self,self.opponent)

    def draw_step(self):#抓牌步骤（Draw Step）通常情况下，玩家在这一步抓一张牌。
        self.draw_card(1)


    def inGame_state(self):# 切换到inGame_state
        pass

    async def ending_phase(self):#结束阶段 清空法术力（包括敌方）
        self.end_step()
        await self.cleanup_step()
        

    def end_step(self):#结束步骤（End Step）：某些卡牌效果会在这个时候触发。
        for card in self.get_cards_from_dict("end_step"):
            card.when_end_turn(self,self.opponent)

    async def cleanup_step(self):#清理步骤（Cleanup Step）：玩家将手牌调整至最大手牌限制，移除所有“直到回合结束”类的效果，并移除所有受到的伤害。清空法术力（包括敌方）
        self.mana={"colorless":0,"U":0,"W":0,"B":0,"R":0,"G":0}
        self.opponent.mana={"colorless":0,"U":0,"W":0,"B":0,"R":0,"G":0}

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
            'library':self.library
        }
        if type in deck_type and card in deck_type[type]:
            deck_type[type].remove(card)

        """
        还没有写完代码，要发消息给client，让client做此动作
        """

        self.action_store.append(actions.Lose_Card(self,self,card,False))# 一定是需要的，这个动作


    def append_card(self,card:Card,type:str):#会发送消息给client
        deck_type={
            'battlefield':self.battlefield,
            'hand':self.hand,
            'land_area':self.land_area,
            'graveyard':self.graveyard,
            'library':self.library
        }
        
        if type in deck_type:
            deck_type[type].append(card)
        
        self.action_store.append(actions.Gain_Card(self,self,card,False))

    def mana_consumed(self,card:"Card"):#自己的魔力池减少
        cost=card.cost
        for key in cost:
            self.mana[key]-=cost[key]
        if self.mana["colorless"]<0:
            for key in self.mana:
                if key!="colorless":
                    while self.mana[key]>0 and self.mana["colorless"]<0:
                        self.mana[key]-=1
                        self.mana["colorless"]+=1

    def text(self,player)-> str:
        if self==player:
            return f"player({self.name},Self)"
        else:
            return f"player({self.name},Opponent)"


    
if __name__=="__main__":

    
    
    player=Player("caesar","Mystic Tides+Instant+1|Mystic Reflection+Instant+1|Mystic Evasion+Instant+2|Mindful Manipulation+Sorcery+1|Nyxborn Serpent+Creature+1|Mistweaver Drake+Creature+1",[])
    print(player.deck)
    