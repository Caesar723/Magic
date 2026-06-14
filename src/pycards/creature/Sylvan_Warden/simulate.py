from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Sylvan_Warden.model import Sylvan_Warden

@bind_card(Sylvan_Warden)
class Sylvan_Warden_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you may search your library for a basic land card and put it onto the battlefield tapped. If you do, shuffle your library. Whenever [CARD_NAME] attacks, you may put a +1/+1 counter on target creature you control.",

        "When [CARD_NAME] enters play, you may search for a basic land, put it onto the battlefield tapped, and shuffle. Whenever [CARD_NAME] attacks, you may put a +1/+1 counter on target creature you control.",

        "As [CARD_NAME] enters the battlefield, you may search your library for a basic land, put it onto the battlefield tapped, shuffle if you do. Whenever [CARD_NAME] attacks, you may put a +1/+1 counter on target creature you control.",

        "Upon entering the battlefield, [CARD_NAME] lets you search for a basic land and put it onto the battlefield tapped, then shuffle. Whenever [CARD_NAME] attacks, you may put a +1/+1 counter on target creature you control.",

        "When [CARD_NAME] arrives, you may search for a basic land, put it onto the battlefield tapped, shuffle. Whenever [CARD_NAME] attacks, you may put a +1/+1 counter on target creature you control.",

        "When [CARD_NAME] enters the battlefield, you may find a basic land, put it onto the battlefield tapped, shuffle if you do. Whenever [CARD_NAME] attacks, you may put a +1/+1 counter on target creature you control.",

        "When [CARD_NAME] enters the battlefield, you may search your library for a basic land card, put it onto the battlefield tapped, shuffle if you do. On attack, you may put a +1/+1 counter on target creature you control.",

        "When [CARD_NAME] enters the battlefield, you may search for a basic land and put it onto the battlefield tapped, then shuffle. Each time [CARD_NAME] attacks, you may put a +1/+1 counter on target creature you control.",

        "When [CARD_NAME] enters the battlefield, you may search your library for a basic land, put it onto the battlefield tapped, shuffle if you do. Whenever [CARD_NAME] attacks, you may place a +1/+1 counter on target creature you control.",

    ]
