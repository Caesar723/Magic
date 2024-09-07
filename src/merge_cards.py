from initinal_file import CARD_DICTION,ORGPATH
import json
from game.type_cards.creature import Creature
from game.type_cards.instant import Instant,Instant_Undo
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery


def merge_creature_cards():
    for creature_class in Creature.__subclasses__():
        card_info=get_card_info(creature_class)
        name=card_info["Name"]
        try:
            with open(f"{ORGPATH}/cards/creature/{name}/data.json",'r') as f:
                existing_data = {}
                existing_data = json.load(f)
            flag=False
            print("*"*100)
            for key in card_info:
                if card_info[key]!=existing_data[key]:
                    flag=True
                    print(f"The card {name} has different data in the database and the card file!")
                    print(f"key:{key}")
                    print(f"existing_data:{existing_data[key]}!",type(existing_data[key]))
                    print(f"card_info:{card_info[key]}!",type(card_info[key]))
                    existing_data[key]=card_info[key]
                    
            if flag:
                print(f"The card {name} has different data in the database and the card file!")
                print(existing_data)
                print(card_info)
                
                with open(f"{ORGPATH}/cards/creature/{name}/data.json",'w') as f:
                    json.dump(existing_data,f,indent=4)
                # pass
            else:
                
                print(f"The card {name} has the same data in the database and the card file!")
            print("*"*100)
            print("\n"*2)
        except Exception as e:
            print(e)  
    

def merge_instant_cards():
    for instant_class in Instant.__subclasses__():
        card_info=get_card_info(instant_class)
        if card_info==False:continue
        name=card_info["Name"]
        try:
            with open(f"{ORGPATH}/cards/Instant/{name}/data.json",'r') as f:
                existing_data = {}
                existing_data = json.load(f)    
            flag=False
            print("*"*100)
            for key in card_info:
                if card_info[key]!=existing_data[key]:
                    flag=True
                    existing_data[key]=card_info[key]
                    print(f"The card {name} has different data in the database and the card file!")
                    print(f"key:{key}")
                    print(f"existing_data:{existing_data[key]}!",type(existing_data[key]))
                    print(f"card_info:{card_info[key]}!",type(card_info[key]))
            if flag:
                print(f"The card {name} has different data in the database and the card file!")
                print(existing_data)
                print(card_info)
                
                with open(f"{ORGPATH}/cards/Instant/{name}/data.json",'w') as f:
                    json.dump(existing_data,f,indent=4)
                # pass
            else:
                print(f"The card {name} has the same data in the database and the card file!")
            print("*"*100)
            print("\n"*2)
        except Exception as e:
            print(e)  
            print(card_info)

def merge_land_cards():
    for land_class in Land.__subclasses__():
        card_info=get_card_info(land_class)
        name=card_info["Name"]
        try:
            with open(f"{ORGPATH}/cards/land/{name}/data.json",'r') as f:
                existing_data = {}
                existing_data = json.load(f)
            flag=False
            print("*"*100)
            for key in card_info:
                if card_info[key]!=existing_data[key]:
                    flag=True
                    existing_data[key]=card_info[key]
                    print(f"The card {name} has different data in the database and the card file!")
                    print(f"key:{key}")
                    print(f"existing_data:{existing_data[key]}!")
                    print(f"card_info:{card_info[key]}!")
            if flag:
                print(f"The card {name} has different data in the database and the card file!")
                print(existing_data)
                print(card_info)
                
                with open(f"{ORGPATH}/cards/land/{name}/data.json",'w') as f:
                    json.dump(existing_data,f,indent=4)
                # pass
            else:
                
                print(f"The card {name} has the same data in the database and the card file!")
            print("*"*100)
            print("\n"*2)
        except Exception as e:
            print(e)  

def merge_sorcery_cards():
    for sorcery_class in Sorcery.__subclasses__():
        card_info=get_card_info(sorcery_class)
        
        name=card_info["Name"]
        #try:
        with open(f"{ORGPATH}/cards/sorcery/{name}/data.json",'r') as f:
            existing_data = {}
            existing_data = json.load(f)
            flag=False
            print("*"*100)
            for key in card_info:
                if card_info[key]!=existing_data[key]:
                    flag=True
                    existing_data[key]=card_info[key]
                    print(f"The card {name} has different data in the database and the card file!")
                    print(f"key:{key}")
                    print(f"existing_data:{existing_data[key]}!",type(existing_data[key]))
                    print(f"card_info:{card_info[key]}!",type(card_info[key]))
            if flag:
                print(f"The card {name} has different data in the database and the card file!")
                print(existing_data)
                print(card_info)
                
                with open(f"{ORGPATH}/cards/sorcery/{name}/data.json",'w') as f:
                    json.dump(existing_data,f,indent=4)
                # pass
            else:
                
                print(f"The card {name} has the same data in the database and the card file!")
            print("*"*100)
            print("\n"*2)
        #except Exception as e:
            #print(e)  
            #print(card_info)

def get_card_info(card_class):
    if (card_class==Instant_Undo):return False
    card:"Creature|Instant|Land|Sorcery"=card_class(None)
    if issubclass(card_class,Creature):
        parameters={"Name":card.name,"Rarity":card.rarity,"Type":card.type_card,"Power":int(card.power),"Toughness":int(card.live),"Cost":card.mana_cost,"Ability":card.content}
    elif issubclass(card_class,Instant):
        parameters={"Name":card.name,"Rarity":card.rarity,"Cost":card.mana_cost,"Ability":card.content}
    elif issubclass(card_class,Land):
        parameters={"Name":card.name,"Rarity":card.rarity,"Type":card.type,"Ability":card.content}
    elif issubclass(card_class,Sorcery):
        parameters={"Name":card.name,"Rarity":card.rarity,"Cost":card.mana_cost,"Ability":card.content}
    return parameters

#让src/cards里所有的文件夹的名字尾部没有空格


def remove_trailing_spaces(directory):
    import os
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if dir_name.endswith(' '):
                new_dir_name = dir_name.rstrip()
                os.rename(os.path.join(root, dir_name), os.path.join(root, new_dir_name))
                print(f"Renamed: {dir_name} -> {new_dir_name}!")
if __name__=="__main__":
    #remove_trailing_spaces(f"{ORGPATH}/cards")
    merge_creature_cards()
    merge_instant_cards()
    merge_land_cards()
    merge_sorcery_cards()