

from game.rogue.base_card_batch import BaseCardBatch



class Break_the_Hourglass(BaseCardBatch):
    name:str="Break the Hourglass"
    price:int=30
    background:str="Chronostrider"
    image_path:str="cards/creature/Chronostrider/image.jpg"
    content:str="Add 1 Chronostrider to your deck \n (2/4 3G Flash, Haste. When Chronostrider enters the battlefield, you may take an extra turn after this one.)"


    cards=[
        {
            "name":"Chronostrider",
            "type_card":"Creature",
            "number":1,
        }
    ]
    

        