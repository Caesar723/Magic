from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Dreamweaver_Archivist.model import Dreamweaver_Archivist

@bind_card(Dreamweaver_Archivist)
class Dreamweaver_Archivist_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you may draw a card. If you do, discard a card.",

        "When [CARD_NAME] enters play, you may draw a card. If you do, discard a card.",

        "As [CARD_NAME] enters the battlefield, you may draw a card. If you do, discard a card.",

        "Upon entering the battlefield, [CARD_NAME] lets you draw a card. If you do, discard a card.",

        "When [CARD_NAME] arrives, you may draw a card. If you do, discard a card.",

        "When [CARD_NAME] enters the battlefield, you may draw a card, then discard a card.",

        "When [CARD_NAME] enters the battlefield, you may draw one card. If you do, discard one card.",

        "When [CARD_NAME] enters the battlefield, you may draw a card and discard a card.",

        "When [CARD_NAME] enters the battlefield, you may draw a card. If you do, you discard a card.",

    ]
