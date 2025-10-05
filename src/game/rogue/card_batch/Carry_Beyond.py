

from game.rogue.base_card_batch import BaseCardBatch



class Carry_Beyond(BaseCardBatch):
    name:str="Carry Beyond"
    price:int=30
    background:str="Celestial_Herald"
    image_path:str="cards/creature/Celestial Herald/image.jpg"
    content:str="Add 1 Celestial_Herald to your deck \n (3/3 1w Flying, Lifelink. At the beginning of your upkeep, exile random nonland opponent's permanent. Return that permanent to the battlefield under its owner's control at the beginning of the next end step.)"


    cards=[
        {
            "name":"Celestial Herald",
            "type_card":"Creature",
            "number":1,
        }
    ]
    

        