from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Thundering_Behemoth.model import Thundering_Behemoth

@bind_card(Thundering_Behemoth)
class Thundering_Behemoth_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Trample. When [CARD_NAME] enters the battlefield, creatures you control gain trample until end of turn.",

        "Trample. When [CARD_NAME] enters play, creatures you control gain trample until end of turn.",

        "Trample. As [CARD_NAME] enters the battlefield, creatures you control gain trample until end of turn.",

        "Trample. Upon entering the battlefield, [CARD_NAME] grants trample to creatures you control until end of turn.",

        "Trample. When [CARD_NAME] arrives, creatures you control gain trample until end of turn.",

        "Trample. When [CARD_NAME] enters the battlefield, your creatures gain trample until end of turn.",

        "Trample. When [CARD_NAME] enters the battlefield, all creatures you control gain trample until end of turn.",

        "Trample. When [CARD_NAME] enters the battlefield, creatures under your control gain trample until end of turn.",

        "Trample. When [CARD_NAME] enters the battlefield, creatures you control have trample until end of turn.",

    ]
