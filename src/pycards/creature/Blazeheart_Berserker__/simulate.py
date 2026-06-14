from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Blazeheart_Berserker__.model import Blazeheart_Berserker__

@bind_card(Blazeheart_Berserker__)
class Blazeheart_Berserker___Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Whenever [CARD_NAME] attacks, it gets +1/+0 until end of turn for each Mountain you control.",

        "Each time [CARD_NAME] attacks, it gains +1/+0 until end of turn for every Mountain you control.",

        "When [CARD_NAME] attacks, it receives +1/+0 until end of turn per Mountain under your control.",

        "Whenever [CARD_NAME] swings, it gets +1/+0 until end of turn for each Mountain you have.",

        "On attack, [CARD_NAME] gains +1/+0 until end of turn for every Mountain you control.",

        "Whenever [CARD_NAME] attacks, add +1/+0 until end of turn for each Mountain you control.",

        "When [CARD_NAME] attacks, its power increases by 1 until end of turn for each Mountain you control.",

        "Whenever [CARD_NAME] attacks, it grows by +1/+0 until end of turn for each Mountain you control.",

        "Each attack by [CARD_NAME] grants it +1/+0 until end of turn for every Mountain you control.",

    ]
