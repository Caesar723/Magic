from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Mystic_Insight.model import Mystic_Insight

@bind_card(Mystic_Insight)
class Mystic_Insight_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Scry 2, then draw a card.",

        "[CARD_NAME] lets you scry 2, then draw a card.",

        "Scry 2. Then draw a card.",

        "[CARD_NAME] causes you to scry 2, then draw a card.",

        "Look at the top two cards of your library, put any number on the bottom and the rest on top, then draw a card.",

        "[CARD_NAME] allows you to scry 2 and then draw a card.",

        "Scry two, then draw one card.",

        "[CARD_NAME] scrys 2, then you draw a card.",

        "Scry 2, then draw one card from your library.",

        "[CARD_NAME] lets you scry 2 and draw a card."
    ]
