from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Mistweaver_Drake.model import Mistweaver_Drake

@bind_card(Mistweaver_Drake)
class Mistweaver_Drake_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flash (You may cast this spell any time you could cast an instant).",

        "Flash.",

        "Flash (castable any time you could cast an instant).",

        "Flash (you may cast this as though it were an instant).",

        "Flash (can be cast at instant speed).",

        "Flash (cast at instant speed).",

        "Flash (may be cast any time you could cast an instant).",

        "Flash (this may be cast as an instant).",

        "Flash (you can cast this any time you could cast an instant).",

    ]
