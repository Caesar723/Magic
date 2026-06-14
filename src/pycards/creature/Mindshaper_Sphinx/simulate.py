from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Mindshaper_Sphinx.model import Mindshaper_Sphinx

@bind_card(Mindshaper_Sphinx)
class Mindshaper_Sphinx_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flying. When [CARD_NAME] enters the battlefield, scry 3, then draw a card.",

        "Flying. When [CARD_NAME] enters play, scry 3, then draw a card.",

        "Flying. As [CARD_NAME] enters the battlefield, scry 3, then draw a card.",

        "Flying. Upon entering the battlefield, [CARD_NAME] lets you scry 3, then draw a card.",

        "Flying. When [CARD_NAME] arrives, scry 3, then draw a card.",

        "Flying. When [CARD_NAME] enters the battlefield, scry three, then draw a card.",

        "Flying. When [CARD_NAME] enters the battlefield, scry 3 and then draw a card.",

        "Flying. When [CARD_NAME] enters the battlefield, scry 3, then draw one card.",

        "Flying. When [CARD_NAME] enters the battlefield, scry 3 followed by drawing a card.",

    ]
