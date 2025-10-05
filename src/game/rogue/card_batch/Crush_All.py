

from game.rogue.base_card_batch import BaseCardBatch



class Crush_All(BaseCardBatch):
    name:str="Crush All"
    price:int=99
    background:str="Blightsteel Colossus"
    image_path:str="cards/creature/Blightsteel Colossus/image.jpg"
    content:str="Add 1 Blightsteel Colossus to your deck \n (11/11 12 Trample, Infect (This creature deals damage to creatures in the form of -1/-1 counters and to players in the form of poison counters.), Indestructible (This creature can't be destroyed by damage or effects that say \"destroy.\"))"


    cards=[
        {
            "name":"Blightsteel Colossus",
            "type_card":"Creature",
            "number":1,
        }
    ]
    

        