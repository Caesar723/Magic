from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Honorable_Protection.model import Honorable_Protection

@bind_card(Honorable_Protection)
class Honorable_Protection_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target creature you control gains indestructible until end of turn. If it's a Knight, put a +1/+1 counter on it.",
        "[CARD_NAME] gives a creature you control indestructible until end of turn; Knights get a +1/+1 counter.",
        "Choose a creature you control. Indestructible until end of turn. +1/+1 counter if it's a Knight.",
        "Grant indestructible to target creature you control this turn. Knights also get +1/+1.",
        "[CARD_NAME]: indestructible on your creature; +1/+1 if Knight.",
        "Your creature gains indestructible until end of turn. Put +1/+1 on it if it's a Knight.",
        "Indestructible until end of turn on a creature you control. Knights get +1/+1 counter.",
        "With [CARD_NAME], protect your creature with indestructible; Knights grow +1/+1.",
        "Target your creature: indestructible this turn, +1/+1 if Knight.",
        "[CARD_NAME] makes your creature indestructible and buffs Knights with +1/+1.",
    ]
