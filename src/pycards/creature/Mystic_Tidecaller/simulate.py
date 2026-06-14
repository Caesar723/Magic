from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Mystic_Tidecaller.model import Mystic_Tidecaller

@bind_card(Mystic_Tidecaller)
class Mystic_Tidecaller_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flash. When [CARD_NAME] enters the battlefield, you may return target nonland permanent to its owner's hand.",

        "Flash. When [CARD_NAME] enters play, you may return target nonland permanent to its owner's hand.",

        "Flash. As [CARD_NAME] enters the battlefield, you may return target nonland permanent to its owner's hand.",

        "Flash. Upon entering the battlefield, [CARD_NAME] lets you return target nonland permanent to its owner's hand.",

        "Flash. When [CARD_NAME] arrives, you may return target nonland permanent to its owner's hand.",

        "Flash. When [CARD_NAME] enters the battlefield, you may bounce target nonland permanent.",

        "Flash. When [CARD_NAME] enters the battlefield, you may return target nonland permanent to hand.",

        "Flash. When [CARD_NAME] enters the battlefield, you may return a target nonland permanent to its owner's hand.",

        "Flash. When [CARD_NAME] enters the battlefield, you may return target nonland permanent to its owner's hand.",

    ]
