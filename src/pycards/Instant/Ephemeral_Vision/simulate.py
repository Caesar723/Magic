from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Ephemeral_Vision.model import Ephemeral_Vision

@bind_card(Ephemeral_Vision)
class Ephemeral_Vision_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Draw a card. Scry 2.",
        "[CARD_NAME] lets you draw a card and scry 2.",
        "Draw one card, then scry 2.",
        "With [CARD_NAME], draw a card and look at the top two cards of your library.",
        "Draw a card, then scry two.",
        "[CARD_NAME]: draw a card, scry 2.",
        "Draw a card and scry 2 with [CARD_NAME].",
        "You draw a card, then scry 2.",
        "Draw one, scry two.",
        "[CARD_NAME] draws you a card and lets you scry 2.",
    ]
