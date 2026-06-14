from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Mistweaver_Adept.model import Mistweaver_Adept

@bind_card(Mistweaver_Adept)
class Mistweaver_Adept_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you may return target creature to its owner's hand. If you do, scry 2.",

        "When [CARD_NAME] enters play, you may return target creature to its owner's hand. If you do, scry 2.",

        "As [CARD_NAME] enters the battlefield, you may return target creature to its owner's hand. If you do, scry 2.",

        "Upon entering the battlefield, [CARD_NAME] lets you return target creature to its owner's hand. If you do, scry 2.",

        "When [CARD_NAME] arrives, you may return target creature to its owner's hand. If you do, scry 2.",

        "When [CARD_NAME] enters the battlefield, you may bounce target creature. If you do, scry 2.",

        "When [CARD_NAME] enters the battlefield, you may return target creature to hand. If you do, scry 2.",

        "When [CARD_NAME] enters the battlefield, you may return target creature to its owner's hand, then scry 2 if you do.",

        "When [CARD_NAME] enters the battlefield, you may return target creature to its owner's hand. If you do, scry two.",

    ]
