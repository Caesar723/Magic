from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Fiery_Burst.model import Fiery_Burst

@bind_card(Fiery_Burst)
class Fiery_Burst_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 2 damage to target creature or player.",

        "Deal 2 damage to target creature or player.",

        "[CARD_NAME] deals two damage to target creature or player.",

        "Deal two damage to target creature or player.",

        "[CARD_NAME] inflicts 2 damage on target creature or player.",

        "Target creature or player takes 2 damage.",

        "[CARD_NAME] hits target creature or player for 2 damage.",

        "Deal 2 damage to a target creature or player of your choice.",

        "[CARD_NAME] deals 2 damage to a chosen creature or player.",

        "Choose target creature or player. [CARD_NAME] deals 2 damage to it."
    ]
