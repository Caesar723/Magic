from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Arcane_Inferno.model import Arcane_Inferno

@bind_card(Arcane_Inferno)
class Arcane_Inferno_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 3 damage to any target. If you control a creature with power 5 or greater, it deals 5 damage instead.",
        "Deal 3 damage to any target. If you control a creature with power 5 or greater, deal 5 damage instead.",
        "[CARD_NAME] hits any target for 3 damage, or 5 if you control a creature with power 5 or greater.",
        "Choose any target. [CARD_NAME] deals 3 damage to it, or 5 if you have a creature with power 5+.",
        "Deal 3 damage to any target. Upgrade to 5 damage if you control a creature with power 5 or greater.",
        "[CARD_NAME] inflicts 3 damage on any target, increased to 5 when you control a power-5-or-greater creature.",
        "Any target takes 3 damage from [CARD_NAME], or 5 if a creature you control has power 5 or greater.",
        "Fire 3 damage at any target; deal 5 instead if you control a creature with power 5 or greater.",
        "[CARD_NAME] deals 3 to any target, boosted to 5 when you control a large creature (power 5+).",
        "Deal 3 damage to any target. If you have a creature with power 5 or greater, [CARD_NAME] deals 5 instead.",
    ]
