
from game.rogue.rogue_dict import ROGUE_AGENTS_DICT,ROGUE_TREASURE_DICT,ROGUE_EVENT_DICT




class Base_Event:
    title=""
    description=""
    image=""
    
    options=[]

    @classmethod
    def function_1(cls,player_profile:dict):
        pass

    @classmethod
    def function_2(cls,player_profile:dict):
        pass

    @classmethod
    def function_3(cls,player_profile:dict):
        pass

    @classmethod
    def cheak_valid_1(cls,player_profile:dict):
        return True

    @classmethod
    def cheak_valid_2(cls,player_profile:dict):
        return False

    @classmethod
    def cheak_valid_3(cls,player_profile:dict):
        return True

    @classmethod
    def get_treasure(cls,player_profile:dict):
        pass
    
    

    