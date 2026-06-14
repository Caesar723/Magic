from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Nature_s_Reprisal.model import Nature_s_Reprisal

@bind_card(Nature_s_Reprisal)
class Nature_s_Reprisal_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Destroy target creature with flying. You gain 2 life.",
        "[CARD_NAME] destroys target creature with flying and you gain 2 life.",
        "Choose target flying creature. Destroy it. Gain 2 life.",
        "Destroy a creature with flying. You gain 2 life.",
        "[CARD_NAME]: destroy flying creature, gain 2 life.",
        "Remove target flying creature from the battlefield. Gain 2 life.",
        "Slay a flying creature. You gain 2 life.",
        "With [CARD_NAME], destroy flying creature and gain 2 life.",
        "Target flying creature is destroyed. Gain 2 life.",
        "[CARD_NAME] kills a flyer and grants you 2 life.",
    ]
