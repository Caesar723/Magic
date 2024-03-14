
if __name__=="__main__":
    import sys
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/")
    



from game.action import Action
from game.type_action import actions
from game.card import Card
from initinal_file import CARD_DICTION



  

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

        #mana cost [colorless,red, green, blue,black,white]
        self.mana:list=[]

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
        self.attacker:Card=None

        #defenders
        self.defenders:list[Card]=None

        #游戏还没有开始
        self.deck:list[Card]=[]
        self.initinal_decks(decks_detail)
        self.initinal_card_dict()
    
    def set_opponent_player(self,opponent:"Player"):
        self.opponent=opponent


    def set_socket(self,socket):
        pass

    def send_message(self,type:str,content:str):# the type of content and content
        pass

    def initinal_decks(self,decks_detail:str):#generate cards
        for element in decks_detail.split("|"):
            name,type,number=element.split("+")
            number=int(number)
            self.deck+=[CARD_DICTION[f"{name}_{type}"]() for i in range(number)]
        self.hand=self.deck[:7]# get 7 card to hand
        self.library=self.deck[7:]# the rest is in the library

    def initinal_card_dict(self):# 回合开始，回合结束卡牌，光环。。。
        self.cards_store_dict["upkeep_step"]=[]
        self.cards_store_dict["end_step"]=[]
        self.cards_store_dict["aura"]=[]
        

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

    

    def select_attacker(self,index:int):# select_creature_as_attacker, the index of battlefield
        pass

    def select_defender(self):# select_creature_as_defender
        pass

    def deal_damage_player(self):# Deal damage to player
        pass

    def gain_life_player(self):# gain life to player
        pass

    def when_dealt_damage(self):#when players live decrease
        pass

    def when_gaining_life(self):#when players live increase
        pass

    def play_a_card(self,card:Card):# player 打出一张牌
        result=card.when_use_this_card(self,self.opponent)
        print(result)
        #result[1]()
        return result

    def beginning_phase(self,player:"Player"):#开始阶段
        self.untap_step()
        self.upkeep_step(player)
        self.draw_step()

    def untap_step(self):#解除操控步骤:土地被横置以产生法术力（Mana），生物被横置以攻击等
        pass

    def upkeep_step(self,player:"Player"):#保持步骤（Upkeep Step）：某些卡牌效果会在这个时候触发。
        pass

    def draw_step(self):#抓牌步骤（Draw Step）通常情况下，玩家在这一步抓一张牌。
        self.draw_card(1)


    def inGame_state(self):# 切换到inGame_state
        pass

    def ending_phase(self,player:"Player"):#结束阶段
        pass

    def end_step(self,player:"Player"):#结束步骤（End Step）：某些卡牌效果会在这个时候触发。
        pass

    def cleanup_step(self):#清理步骤（Cleanup Step）：玩家将手牌调整至最大手牌限制，移除所有“直到回合结束”类的效果，并移除所有受到的伤害。
        pass

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
        if type in deck_type and card in deck_type[type]:
            deck_type[type].append(card)

        self.action_store.append(actions.Gain_Card(self,self,card,False))


if __name__=="__main__":

    
    
    player=Player("caesar","Mystic Tides+Instant+1|Mystic Reflection+Instant+1|Mystic Evasion+Instant+2|Mindful Manipulation+Sorcery+1|Nyxborn Serpent+Creature+1|Mistweaver Drake+Creature+1",[])
    print(player.deck)
    