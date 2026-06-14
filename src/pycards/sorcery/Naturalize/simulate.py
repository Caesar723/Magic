from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Naturalize.model import Naturalize

@bind_card(Naturalize)
class Naturalize_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Destroy target creature.",

        "[CARD_NAME] destroys target creature.",

        "Destroy a target creature of your choice.",

        "[CARD_NAME] destroys a chosen target creature.",

        "Target creature is destroyed.",

        "[CARD_NAME] causes target creature to be destroyed.",

        "Choose target creature. Destroy it.",

        "[CARD_NAME] lets you destroy target creature.",

        "Destroy one target creature.",

        "[CARD_NAME] destroys one target creature."
    ]
