from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Mindful_Manipulation.model import Mindful_Manipulation

@bind_card(Mindful_Manipulation)
class Mindful_Manipulation_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Draw two cards, then put one random card from your hand on top of your library.",

        "[CARD_NAME] lets you draw two cards, then place a random card from your hand on top of your library.",

        "Draw two cards. Then put a random card from your hand on top of your deck.",

        "[CARD_NAME] draws you two cards, then moves one random card from your hand to the top of your library.",

        "Draw two cards, then return one random card from your hand to the top of your library.",

        "[CARD_NAME] causes you to draw two cards, then put a random card from your hand on top of your library.",

        "You draw two cards. Then choose a random card from your hand and put it on top of your library.",

        "[CARD_NAME] draws two cards, then sends one random card from your hand to the top of your library.",

        "Draw a pair of cards, then place one random card from your hand on top of your library.",

        "[CARD_NAME] allows you to draw two cards, then put one random card from your hand on top of your library."
    ]
