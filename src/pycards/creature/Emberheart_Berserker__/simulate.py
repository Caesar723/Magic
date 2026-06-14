from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Emberheart_Berserker__.model import Emberheart_Berserker__

@bind_card(Emberheart_Berserker__)
class Emberheart_Berserker___Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Whenever [CARD_NAME] defends, it gets +0/+1 until end of turn for each Mountain you control.",

        "Each time [CARD_NAME] blocks, it gets +0/+1 until end of turn for every Mountain you control.",

        "When [CARD_NAME] defends, it gains +0/+1 until end of turn for each Mountain you control.",

        "Whenever [CARD_NAME] blocks, it gets +0/+1 until end of turn per Mountain you control.",

        "On defense, [CARD_NAME] gets +0/+1 until end of turn for each Mountain you control.",

        "Whenever [CARD_NAME] defends, add +0/+1 until end of turn for each Mountain you control.",

        "When [CARD_NAME] defends, its toughness increases by 1 until end of turn for each Mountain you control.",

        "Whenever [CARD_NAME] defends, it grows by +0/+1 until end of turn for each Mountain you control.",

        "Each block by [CARD_NAME] grants it +0/+1 until end of turn for every Mountain you control.",

    ]
