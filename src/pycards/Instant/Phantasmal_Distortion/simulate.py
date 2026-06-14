from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Phantasmal_Distortion.model import Phantasmal_Distortion

@bind_card(Phantasmal_Distortion)
class Phantasmal_Distortion_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Until end of turn, target creature you control becomes a copy of another your random creature, except it retains its abilities. Return that creature to its owner's hand at the beginning of the next end step.",
        "[CARD_NAME] makes your creature a copy of a random creature you control until end of turn, keeping abilities; bounce at next end step.",
        "Target creature you control copies a random creature of yours this turn, keeping abilities. Bounce at next end step.",
        "Your creature becomes a copy of a random creature you control until end of turn. Return it at next end step.",
        "[CARD_NAME]: copy random own creature on target, retain abilities, bounce next end step.",
        "Until end of turn, your creature copies a random creature you control. Bounce at beginning of next end step.",
        "Transform your creature into a copy of random ally creature this turn. Return to hand next end step.",
        "With [CARD_NAME], copy a random creature you control onto target, keep abilities, bounce later.",
        "Target creature copies random creature you control until EOT; returns to hand next end step.",
        "[CARD_NAME] distorts your creature into a random copy, then bounces it next end step.",
    ]
