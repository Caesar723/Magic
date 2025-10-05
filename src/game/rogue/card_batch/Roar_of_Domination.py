

from game.rogue.base_card_batch import BaseCardBatch



class Roar_of_Domination(BaseCardBatch):
    name:str="Roar of Domination"
    price:int=26
    background:str="Roar of the Behemoth"
    image_path:str="cards/Instant/Roar of the Behemoth/image.jpg"
    content:str="Add 2 Roar of the Behemoth and 2 Titan Giant to your deck \n (All enemy creatures get 0 power until the end of this turn.)"


    cards=[
        {
            "name":"Roar of the Behemoth",
            "type_card":"Instant",
            "number":2,
        },
        {
            "name":"Titan Giant",
            "type_card":"Creature",
            "number":2,
        }
    ]
    

        