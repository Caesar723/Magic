import os
import json
import random


class Pack_Database:#
    
    Percentage_Common=0.65#55%
    Percentage_Uncommon=0.2#30%
    Percentage_Rare=0.1#10%
    Percentage_Mythic_Rare=0.05#5%
    Num_cards=6
    Price=100
    image_url="webpages/image_source/packs/pack_org.jpg"
    ORGPATH=os.path.dirname(os.path.abspath(__file__))
    
   

    def collect_cards(self):#list[]
        Card_contain=[]
        directory=f"{self.ORGPATH}/cards"
        types=os.listdir(directory)
        if ".DS_Store" in types:
            types.remove(".DS_Store")
        for type in types:#creature Instant land sorcery
            further_path=f"{directory}/{type}"
            cards=os.listdir(further_path)
            if ".DS_Store" in cards:
                cards.remove(".DS_Store")
            for card in cards:
                if self.filter_card(card,type,further_path):
                    Card_contain.append(f"cards/{type}/{card}")
        return Card_contain
    
    def filter_card(self,card,type,further_path):#return True or false
        return True


    def draw_cards(self):
        cards_num=[0,0,0,0]#Common_num,Uncommon_num,Rare_num,Mythic_Rare_num
        percentages=[self.Percentage_Common,self.Percentage_Uncommon,self.Percentage_Rare,self.Percentage_Mythic_Rare]
        for i in range(self.Num_cards):
            accu=0
            for percentage_index in range(4):
                accu+=percentages[percentage_index]
                random_val=random.random()
                if random_val<=accu:
                    cards_num[percentage_index]+=1
                    break
        return cards_num


class Pack_generator:
    
    
    def generate_pack(pack_name):
        pass

class Original(Pack_Database):
    Percentage_Common=0.65#55%
    Percentage_Uncommon=0.2#30%
    Percentage_Rare=0.1#10%
    Percentage_Mythic_Rare=0.05#5%
    image_url="webpages/image_source/packs/pack_org.jpg"
    
   

class Legend(Pack_Database):
    Percentage_Common=0.55#55%
    Percentage_Uncommon=0.2#30%
    Percentage_Rare=0.1#10%
    Percentage_Mythic_Rare=0.15#5%
    Num_cards=5
    Price=200
    image_url="webpages/image_source/packs/pack_legend.png"
    
    

class Antiquities(Pack_Database):
    Percentage_Common=0.35#55%
    Percentage_Uncommon=0.5#30%
    Percentage_Rare=0.1#10%
    Percentage_Mythic_Rare=0.05#5%
    Price=150
    image_url="webpages/image_source/packs/pack_antiquities.png"
    
class Red(Pack_Database):
    Num_cards=5
    image_url="webpages/image_source/packs/red.png"
    Price=110
    def filter_card(self,card,type,further_path):#return True or false
        method={"Cost":"R","Type":"Fire"}
        with open(f"{further_path}/{card}/data.json", 'r') as file:
            # 加载JSON文件内容到一个Python字典
            data = json.load(file)
        for color in method:
            if color in data and method[color] in data[color]:
                return True
        return False


class Green(Pack_Database):
    Num_cards=5
    image_url="webpages/image_source/packs/green.png"
    Price=110
    def filter_card(self,card,type,further_path):#return True or false
        method={"Cost":"G","Type":"Forest"}
        with open(f"{further_path}/{card}/data.json", 'r') as file:
            # 加载JSON文件内容到一个Python字典
            data = json.load(file)
        for color in method:
            if color in data and method[color] in data[color]:
                return True
        return False

class Blue(Pack_Database):
    Num_cards=5
    image_url="webpages/image_source/packs/blue.png"
    Price=110
    def filter_card(self,card,type,further_path):#return True or false
        method={"Cost":"U","Type":"Water"}
        with open(f"{further_path}/{card}/data.json", 'r') as file:
            # 加载JSON文件内容到一个Python字典
            data = json.load(file)
        for color in method:
            if color in data and method[color] in data[color]:
                return True
        return False

class Black(Pack_Database):
    Num_cards=5
    image_url="webpages/image_source/packs/black.png"
    Price=110
    def filter_card(self,card,type,further_path):#return True or false
        method={"Cost":"B","Type":"Dark"}
        with open(f"{further_path}/{card}/data.json", 'r') as file:
            # 加载JSON文件内容到一个Python字典
            data = json.load(file)
        for color in method:
            if color in data and method[color] in data[color]:
                return True
        return False

class White(Pack_Database):
    Num_cards=5
    image_url="webpages/image_source/packs/white.png"
    Price=110
    def filter_card(self,card,type,further_path):#return True or false
        method={"Cost":"W","Type":"Light"}
        with open(f"{further_path}/{card}/data.json", 'r') as file:
            # 加载JSON文件内容到一个Python字典
            data = json.load(file)
        for color in method:
            if color in data and method[color] in data[color]:
                return True
        return False



Packs_Dict={}#used to store Pack name and Pack class
for cla in Pack_Database.__subclasses__():
    Packs_Dict[cla.__name__]=cla


def main():
    pass


if __name__=="__main__":
    main()