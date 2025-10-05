




from game.rogue.base_card_batch import BaseCardBatch



class Land_Red(BaseCardBatch):
    name:str="Land Red"
    price:int=10
    background:str="Mountain"
    image_path:str="cards/land/Mountain/image.jpg"
    content:str="Add 4 Mountain to your deck \n (generate 1 red mana)"


    cards=[
        {
            "name":"Mountain",
            "type_card":"Land",
            "number":4,
        },
        
    ]
    

        