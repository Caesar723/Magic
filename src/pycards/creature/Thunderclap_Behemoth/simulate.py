from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Thunderclap_Behemoth.model import Thunderclap_Behemoth

@bind_card(Thunderclap_Behemoth)
class Thunderclap_Behemoth_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Trample. Whenever [CARD_NAME] attacks, it deals 3 damage to each creature defending player controls if you control another creature with power 4 or greater.",

        "Trample. Each time [CARD_NAME] attacks, it deals 3 damage to each creature defending player controls if you control another creature with power 4 or greater.",

        "Trample. When [CARD_NAME] attacks, it deals 3 damage to each creature defending player controls if you have another creature with power 4 or greater.",

        "Trample. On attack, [CARD_NAME] deals 3 damage to each creature defending player controls if you control another creature with power 4+.",

        "Trample. Whenever [CARD_NAME] attacks, if you control another creature with power 4 or greater, it deals 3 damage to each creature defending player controls.",

        "Trample. Whenever [CARD_NAME] attacks, it deals 3 damage to each defending creature if you control another creature with power 4 or greater.",

        "Trample. Whenever [CARD_NAME] attacks, it deals 3 damage to each creature the defending player controls if you control another creature with power 4 or greater.",

        "Trample. Whenever [CARD_NAME] attacks, it deals 3 damage to each creature defending player controls when you control another creature with power 4 or greater.",

        "Trample. Whenever [CARD_NAME] attacks, it deals 3 damage to each creature defending player controls if another creature you control has power 4 or greater.",

    ]
