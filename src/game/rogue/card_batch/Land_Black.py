




from game.rogue.base_card_batch import BaseCardBatch



class Land_Black(BaseCardBatch):
    name:str="Land Black"
    price:int=10
    background:str="Swamp"
    image_path:str="cards/land/Swamp/image.jpg"
    content:str="Add 4 Swamp to your deck \n (generate 1 black mana)"


    cards=[
        {
            "name":"Swamp",
            "type_card":"Land",
            "number":4,
        },
        
    ]
    

        