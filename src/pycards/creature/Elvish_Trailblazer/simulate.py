from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Elvish_Trailblazer.model import Elvish_Trailblazer

@bind_card(Elvish_Trailblazer)
class Elvish_Trailblazer_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Reach. When [CARD_NAME] enters the battlefield, you may search your library for a basic land card, reveal it, and put it into your hand. If you do, shuffle your library.",

        "Reach. When [CARD_NAME] enters play, you may search your library for a basic land, reveal it, put it into your hand, then shuffle.",

        "Reach. As [CARD_NAME] enters the battlefield, you may search your library for a basic land card, reveal it, and add it to your hand. Shuffle if you do.",

        "Reach. Upon entering the battlefield, [CARD_NAME] lets you search for a basic land, reveal it, put it in your hand, and shuffle.",

        "Reach. When [CARD_NAME] arrives, you may search your library for a basic land card, reveal it, put it into your hand, and shuffle.",

        "Reach. When [CARD_NAME] enters the battlefield, you may find a basic land in your library, reveal it, put it into your hand, then shuffle.",

        "Reach. When [CARD_NAME] enters the battlefield, you may search your library for a basic land card, reveal it, add it to your hand, and shuffle.",

        "Reach. When [CARD_NAME] enters the battlefield, you may search for a basic land card, reveal it, put it into your hand. Shuffle your library if you do.",

        "Reach. When [CARD_NAME] enters the battlefield, you may search your library for a basic land, reveal it, place it in your hand, and shuffle.",

    ]
