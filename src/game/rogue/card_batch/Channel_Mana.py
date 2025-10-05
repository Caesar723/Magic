

from game.rogue.base_card_batch import BaseCardBatch



class Channel_Mana(BaseCardBatch):
    name:str="Channel Mana"
    price:int=16
    background:str="Channel Mana"
    image_path:str="cards/creature/Essence Channeler/image.jpg"
    content:str="Add 4 Essence Channeler to your deck \n (2/2 1G Whenever you cast a creature spell, you may add G to your mana pool.)"


    cards=[
        {
            "name":"Essence Channeler",
            "type_card":"Creature",
            "number":4,
        }
    ]
    

        