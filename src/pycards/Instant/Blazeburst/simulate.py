from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Blazeburst.model import Blazeburst

@bind_card(Blazeburst)
class Blazeburst_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 3 damage to any target.",
        "Deal 3 damage to any target.",
        "[CARD_NAME] hits any target for 3 damage.",
        "Choose any target. [CARD_NAME] deals 3 damage to it.",
        "Fire 3 damage at any target.",
        "[CARD_NAME] inflicts 3 damage on any target.",
        "Any target takes 3 damage from [CARD_NAME].",
        "Deal three damage to any target with [CARD_NAME].",
        "[CARD_NAME] strikes any target for 3 damage.",
        "Target anything; [CARD_NAME] deals 3 damage to it.",
    ]
