




from game.rogue.base_card_batch import BaseCardBatch



class Land_White(BaseCardBatch):
    name:str="Land White"
    price:int=10
    background:str="Plains"
    image_path:str="cards/land/Plains/image.jpg"
    content:str="Add 4 Plains to your deck \n (generate 1 white mana)"


    cards=[
        {
            "name":"Plains",
            "type_card":"Land",
            "number":4,
        },
        
    ]
    

        