



class BaseCardBatch:

    name=""
    cards=[]
    content=""
    price=0
    background=""
    image_path=""


    @classmethod
    def put_card_to_deck(cls,deck:dict):
        
        for card in cls.cards:
            flag=False
            for card_dict in deck:
                if card_dict["name"]==card["name"] and card_dict["type_card"]==card["type_card"]:
                    card_dict["number"]+=card["number"]
                    flag=True
                    break
            if not flag:
                deck.append(card.copy())