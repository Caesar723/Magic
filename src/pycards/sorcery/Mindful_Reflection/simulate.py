from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Mindful_Reflection.model import Mindful_Reflection

@bind_card(Mindful_Reflection)
class Mindful_Reflection_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Draw two cards, then discard a card.",

        "[CARD_NAME] lets you draw two cards, then discard a card.",

        "Draw two cards. Then discard a card.",

        "[CARD_NAME] draws you two cards, then you discard a card.",

        "Draw two cards, then discard one card from your hand.",

        "[CARD_NAME] causes you to draw two cards, then discard a card.",

        "You draw two cards, then discard a card.",

        "[CARD_NAME] allows you to draw two cards and then discard a card.",

        "Draw a pair of cards, then discard one card.",

        "[CARD_NAME] draws two cards, then you discard a card."
    ]
