from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Sunlit_Priestess.model import Sunlit_Priestess

@bind_card(Sunlit_Priestess)
class Sunlit_Priestess_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you gain 3 life.",

        "When [CARD_NAME] enters play, you gain 3 life.",

        "As [CARD_NAME] enters the battlefield, you gain 3 life.",

        "Upon entering the battlefield, [CARD_NAME] causes you to gain 3 life.",

        "When [CARD_NAME] arrives, you gain 3 life.",

        "When [CARD_NAME] enters the battlefield, your life total increases by 3.",

        "When [CARD_NAME] enters the battlefield, you gain three life.",

        "When [CARD_NAME] enters the battlefield, you restore 3 life.",

        "When [CARD_NAME] enters the battlefield, gain 3 life.",

    ]
