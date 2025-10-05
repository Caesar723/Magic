




from game.rogue.base_card_batch import BaseCardBatch



class Land_Blue(BaseCardBatch):
    name:str="Land Blue"
    price:int=10
    background:str="Island"
    image_path:str="cards/land/Island/image.jpg"
    content:str="Add 4 Island to your deck \n (generate 1 blue mana)"


    cards=[
        {
            "name":"Island",
            "type_card":"Land",
            "number":4,
        },
        
    ]
    

        