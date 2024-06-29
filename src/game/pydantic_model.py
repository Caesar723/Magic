
from pydantic import BaseModel



class CardPara(BaseModel):#infomation to create cards:(color,name,type_card,rarity,content,image_path,mana_cost) 
    mana_cost:str
    color:str
    name:str
    type_card:str
    rarity:str
    content:str
    image_path:str

class CreaturePara(CardPara):
    live:int
    power:int
    type_creature:str
    

class LandPara(CardPara):
    pass


    