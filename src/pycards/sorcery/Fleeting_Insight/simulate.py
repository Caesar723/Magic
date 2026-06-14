from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Fleeting_Insight.model import Fleeting_Insight

@bind_card(Fleeting_Insight)
class Fleeting_Insight_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Draw a card, then randomly discard a card.",

        "[CARD_NAME] lets you draw a card, then randomly discard a card.",

        "Draw one card, then randomly discard a card.",

        "[CARD_NAME] draws you a card, then you randomly discard a card.",

        "Draw a card. Then randomly discard a card.",

        "[CARD_NAME] causes you to draw a card, then randomly discard a card.",

        "You draw a card, then randomly discard a card.",

        "[CARD_NAME] allows you to draw a card and then randomly discard a card.",

        "Draw a card, then discard a random card from your hand.",

        "[CARD_NAME] draws a card, then you randomly discard a card."
    ]
