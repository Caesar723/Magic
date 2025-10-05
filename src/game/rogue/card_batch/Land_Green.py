




from game.rogue.base_card_batch import BaseCardBatch



class Land_Green(BaseCardBatch):
    name:str="Land Green"
    price:int=10
    background:str="Forest"
    image_path:str="cards/land/Forest/image.jpg"
    content:str="Add 4 Forest to your deck \n (generate 1 green mana)"


    cards=[
        {
            "name":"Forest",
            "type_card":"Land",
            "number":4,
        },
        
    ]
    

        