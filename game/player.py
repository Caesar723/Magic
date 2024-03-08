
if __name__=="__main__":
    import sys
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/")




from game.action import Action
from game.card import Card






class Player:

    def __init__(self,name:str,decks_detail:str) -> None:

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
        self.action_store:list[Action]=[]

        #state of player Beginning Phase,In-Game State,Ending Phase
        self.state_of_gaming:str=""

        #attacker
        self.attacker:Card=None

        #defenders
        self.defenders:list[Card]=None

        #游戏还没有开始
        self.deck:list[Card]=[]
        self.initinal_decks(decks_detail)
    
    def initinal_decks(self,decks_detail:str):#generate cards
        for element in decks_detail.split("|"):
            name,type,number=element.split("+")
            number=int(number)
            self.deck+=[CARD_DICTION[f"{name}_{type}"]() for i in range(number)]

        

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

    def beginning_phase(self):# when this player start his turn(解除操控步骤，维持步骤，抓牌步骤)
        pass
        

    def ending_phase(self):# when this player end his turn(结束步骤，清理步骤[卡牌])
        pass

    def select_attacker(self):# select_creature_as_attacker
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
        pass

if __name__=="__main__":

    from pycards import *
    from initinal_file import CARD_DICTION
    player=Player("caesar","Mystic Tides+Instant+1|Mystic Reflection+Instant+1|Mystic Evasion+Instant+2|Mindful Manipulation+Sorcery+1|Nyxborn Serpent+Creature+1|Mistweaver Drake+Creature+1")
    