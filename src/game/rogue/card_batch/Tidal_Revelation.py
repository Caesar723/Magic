

from game.rogue.base_card_batch import BaseCardBatch



class Tidal_Revelation(BaseCardBatch):
    name:str="Tidal Revelation"
    price:int=22
    background:str="Thalassian Tidecaller"
    image_path:str="cards/creature/Thalassian Tidecaller/image.jpg"
    content:str="Add 4 Tidal Revelation to your deck \n (2/2 1U Whenever you cast a blue spell, you may draw a card.)"


    cards=[
        {
            "name":"Thalassian Tidecaller",
            "type_card":"Creature",
            "number":4,
        }
    ]
    

        