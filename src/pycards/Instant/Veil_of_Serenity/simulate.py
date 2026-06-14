from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Veil_of_Serenity.model import Veil_of_Serenity

@bind_card(Veil_of_Serenity)
class Veil_of_Serenity_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Exile target creature spell.",
        "[CARD_NAME] exiles target creature spell.",
        "Choose target creature spell. Exile it.",
        "Exile a creature spell on the stack.",
        "[CARD_NAME]: exile target creature spell.",
        "Remove target creature spell from the game by exiling it.",
        "Target creature spell is exiled.",
        "With [CARD_NAME], exile a creature spell.",
        "Banish target creature spell.",
        "[CARD_NAME] exiles creature spells from the stack.",
    ]
