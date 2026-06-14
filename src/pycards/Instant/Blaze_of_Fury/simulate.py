from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Blaze_of_Fury.model import Blaze_of_Fury

@bind_card(Blaze_of_Fury)
class Blaze_of_Fury_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 3 damage to any target. If a creature is dealt damage this way, tap it.",
        "Deal 3 damage to any target. If a creature is dealt damage this way, tap it.",
        "[CARD_NAME] hits any target for 3. Tap any creature damaged this way.",
        "Choose any target. Deal 3 damage. Tap creatures damaged this way.",
        "Deal 3 damage to any target; tap creatures that take damage from [CARD_NAME].",
        "[CARD_NAME] deals 3 to any target and taps creatures damaged by it.",
        "Any target takes 3 damage. Tap creatures dealt damage this way.",
        "Inflict 3 damage on any target. Tap creatures damaged by [CARD_NAME].",
        "Deal 3 damage to any target. Creatures damaged this way become tapped.",
        "[CARD_NAME]: 3 damage to any target; tap creatures hit this way.",
    ]
