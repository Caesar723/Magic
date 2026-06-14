from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Naturalize.model import Naturalize

@bind_card(Naturalize)
class Naturalize_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Destroy target creature.",
        "[CARD_NAME] destroys target creature.",
        "Choose target creature. Destroy it.",
        "Destroy a creature.",
        "[CARD_NAME] removes target creature from the battlefield.",
        "Target creature is destroyed.",
        "Slay target creature with [CARD_NAME].",
        "Eliminate target creature.",
        "[CARD_NAME]: destroy target creature.",
        "Destroy one creature.",
    ]
