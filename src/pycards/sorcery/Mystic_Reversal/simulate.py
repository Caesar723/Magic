from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Mystic_Reversal.model import Mystic_Reversal

@bind_card(Mystic_Reversal)
class Mystic_Reversal_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Each player draws a card, then discards a card.",

        "[CARD_NAME] causes each player to draw a card, then discard a card.",

        "Every player draws a card, then discards a card.",

        "[CARD_NAME] makes each player draw a card and then discard a card.",

        "Each player draws one card, then discards one card.",

        "[CARD_NAME] lets each player draw a card, then discard a card.",

        "All players draw a card, then discard a card.",

        "[CARD_NAME] has each player draw a card, then discard a card.",

        "Each player draws a card. Then each player discards a card.",

        "[CARD_NAME] causes every player to draw a card, then discard a card."
    ]
