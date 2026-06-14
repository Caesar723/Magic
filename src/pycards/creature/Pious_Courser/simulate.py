from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Pious_Courser.model import Pious_Courser

@bind_card(Pious_Courser)
class Pious_Courser_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you gain 2 life.",

        "When [CARD_NAME] enters play, you gain 2 life.",

        "As [CARD_NAME] enters the battlefield, you gain 2 life.",

        "Upon entering the battlefield, [CARD_NAME] causes you to gain 2 life.",

        "When [CARD_NAME] arrives, you gain 2 life.",

        "When [CARD_NAME] enters the battlefield, your life total increases by 2.",

        "When [CARD_NAME] enters the battlefield, you gain two life.",

        "When [CARD_NAME] enters the battlefield, you restore 2 life.",

        "When [CARD_NAME] enters the battlefield, gain 2 life.",

    ]
