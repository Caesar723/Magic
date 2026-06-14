from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Thornroot_Druid.model import Thornroot_Druid

@bind_card(Thornroot_Druid)
class Thornroot_Druid_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you may search your library for a basic land card, reveal it, put it into your hand, then shuffle your library.",

        "When [CARD_NAME] enters play, you may search your library for a basic land, reveal it, put it into your hand, then shuffle.",

        "As [CARD_NAME] enters the battlefield, you may search for a basic land, reveal it, put it in your hand, then shuffle.",

        "Upon entering the battlefield, [CARD_NAME] lets you search for a basic land, reveal it, put it into your hand, then shuffle.",

        "When [CARD_NAME] arrives, you may search your library for a basic land, reveal it, put it into your hand, then shuffle.",

        "When [CARD_NAME] enters the battlefield, you may find a basic land, reveal it, add it to your hand, then shuffle your library.",

        "When [CARD_NAME] enters the battlefield, you may search your library for a basic land card, reveal it, place it in your hand, then shuffle.",

        "When [CARD_NAME] enters the battlefield, you may search for a basic land, reveal it, put it into your hand, and shuffle.",

        "When [CARD_NAME] enters the battlefield, you may search your library for a basic land, reveal it, put it into your hand, then shuffle your library.",

    ]
