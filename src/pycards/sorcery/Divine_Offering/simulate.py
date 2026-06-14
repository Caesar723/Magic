from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Divine_Offering.model import Divine_Offering

@bind_card(Divine_Offering)
class Divine_Offering_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Destroy target land. Its controller gains 3 life.",

        "[CARD_NAME] destroys target land. Its controller gains 3 life.",

        "Destroy a target land. That land's controller gains 3 life.",

        "[CARD_NAME] destroys target land and its controller gains 3 life.",

        "Choose target land. Destroy it. Its controller gains 3 life.",

        "[CARD_NAME] destroys a chosen target land. Its controller gains 3 life.",

        "Target land is destroyed. Its controller gains 3 life.",

        "[CARD_NAME] destroys target land, and its controller gains three life.",

        "Destroy one target land. Its controller gains 3 life.",

        "[CARD_NAME] causes target land to be destroyed. Its controller gains 3 life."
    ]
