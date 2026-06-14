from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Verdant_Genesis.model import Verdant_Genesis

@bind_card(Verdant_Genesis)
class Verdant_Genesis_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Search your library for up to two land cards, put them onto the battlefield tapped, then shuffle your library. You may put a +1/+1 counter on each creature you control.",

        "[CARD_NAME] lets you search for up to two land cards, put them onto the battlefield tapped, shuffle, and optionally put a +1/+1 counter on each creature you control.",

        "Search your library for up to two lands, put them onto the battlefield tapped, shuffle your library. You may put a +1/+1 counter on each creature you control.",

        "[CARD_NAME] searches for up to two land cards, puts them onto the battlefield tapped, shuffles, and you may put a +1/+1 counter on each creature you control.",

        "Find up to two land cards in your library, put them onto the battlefield tapped, shuffle. You may put a +1/+1 counter on each creature you control.",

        "[CARD_NAME] finds up to two lands, puts them onto the battlefield tapped, shuffles your library, and optionally gives each creature you control a +1/+1 counter.",

        "Search for up to two land cards, put them onto the battlefield tapped, shuffle your library. You may put a +1/+1 counter on every creature you control.",

        "[CARD_NAME] allows you to search for up to two lands, put them onto the battlefield tapped, shuffle, and put a +1/+1 counter on each creature you control if you choose.",

        "Search your library for up to two land cards and put them onto the battlefield tapped. Shuffle. You may put a +1/+1 counter on each creature you control.",

        "[CARD_NAME] searches your library for up to two land cards, puts them onto the battlefield tapped, shuffles, and you may put a +1/+1 counter on each creature you control."
    ]
