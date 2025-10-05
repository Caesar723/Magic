

from game.rogue.base_card_batch import BaseCardBatch



class Primal_Interruption(BaseCardBatch):
    name:str="Primal Interruption"
    price:int=32
    background:str="Druid's Natural Fury"
    image_path:str="cards/Instant/Druid's Natural Fury/image.jpg"
    content:str="Add 2 Druid's Natural Fury and 2 Summoner's Arcane Acquisition to your deck \n (Counter target spell)"


    cards=[
        {
            "name":"Summoner's Arcane Acquisition",
            "type_card":"Instant",
            "number":2,
        },
        {
            "name":"Druid's Natural Fury",
            "type_card":"Instant",
            "number":2,
        }
    ]
    

        