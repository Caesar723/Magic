


from game.rogue.base_event import Base_Event

class Mysterious_Ancient_Temple(Base_Event):
    title="Mysterious Ancient Temple"
    description='Deep in the forest, you discover an ancient temple covered in vines. A faint blue glow emanates from its entrance, and the air is thick with ancient magic. Ancient runes carved on the stone door seem to whisper secrets of the past. You sense great power hidden here, but also unknown dangers...'
    image="🏛️"
    @classmethod
    def function_1(cls,player_profile:dict):
        pass

    @classmethod
    def function_2(cls,player_profile:dict):
        pass

    @classmethod
    def function_3(cls,player_profile:dict):
        pass

    
Mysterious_Ancient_Temple.options=[
        {
            "title": "Cautious Exploration",
            "description": 'Carefully enter the temple, paying close attention to traps and clues. Gain +50 EXP and discover a hidden chest.',
            "function": Mysterious_Ancient_Temple.function_1,
            "valid_check":Mysterious_Ancient_Temple.cheak_valid_1
        },
        {
            "title": "Charge In",
            "description": 'Bravely rush deep into the temple, ignoring potential dangers. 50% chance to obtain rare equipment, 50% chance to trigger a trap.',
            "function": Mysterious_Ancient_Temple.function_2,
            "valid_check":Mysterious_Ancient_Temple.cheak_valid_2
        },
        {
            "title": "Leave the Place",
            "description": 'Feeling it’s too dangerous, you decide to leave. You remain in your current state and gain no rewards.',
            "function": Mysterious_Ancient_Temple.function_3,
            "valid_check":Mysterious_Ancient_Temple.cheak_valid_3
        },
        
    ]
        
    