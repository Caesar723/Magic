




from game.rogue.base_card_batch import BaseCardBatch



class Turn_Blows_to_Power(BaseCardBatch):
    name:str="Turn Blows to Power"
    price:int=31
    background:str="Mystic_Convergence"
    image_path:str="cards/Instant/Mystic Convergence/image.jpg"
    content:str="Add 3 Mystic Convergence to Power to your deck \n (2GW Prevent all combat damage that would be dealt this turn. At the beginning of your next main phase, add X mana in any combination of colors to your mana pool, where X is the amount of combat damage prevented this way.)"


    cards=[
        {
            "name":"Mystic Convergence",
            "type_card":"Instant",
            "number":3,
        },
        
    ]
    

        