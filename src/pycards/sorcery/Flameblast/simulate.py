from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Flameblast.model import Flameblast

@bind_card(Flameblast)
class Flameblast_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 5 damage to any target.",

        "Deal 5 damage to any target.",

        "[CARD_NAME] deals five damage to any target.",

        "Deal five damage to any target.",

        "[CARD_NAME] inflicts 5 damage on any target.",

        "Any target takes 5 damage.",

        "[CARD_NAME] hits any target for 5 damage.",

        "Deal 5 damage to a target of your choice.",

        "[CARD_NAME] deals 5 damage to a chosen target.",

        "Choose any target. [CARD_NAME] deals 5 damage to it."
    ]
