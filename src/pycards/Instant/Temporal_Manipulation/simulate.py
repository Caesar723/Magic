from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Temporal_Manipulation.model import Temporal_Manipulation

@bind_card(Temporal_Manipulation)
class Temporal_Manipulation_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Take an extra turn after this one.",
        "[CARD_NAME] lets you take an extra turn after this one.",
        "You take an additional turn after this one.",
        "Gain an extra turn after the current one.",
        "[CARD_NAME]: extra turn after this one.",
        "After this turn, take another turn.",
        "With [CARD_NAME], take an extra turn following this one.",
        "Take one extra turn after this turn ends.",
        "An additional turn after this one.",
        "[CARD_NAME] grants an extra turn after this one.",
    ]
