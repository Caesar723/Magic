from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Torrent_Elemental.model import Torrent_Elemental

@bind_card(Torrent_Elemental)
class Torrent_Elemental_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flash and Flying.",

        "Flying, Flash.",

        "Flying. Flash.",

        "Flying (can't be blocked except by flying or reach) and Flash (cast at instant speed).",

        "Flying and Flash (you may cast this any time you could cast an instant).",

        "Flash and Flying (can be cast at instant speed and can't be blocked except by flying or reach).",

        "Flying, Flash (evasion and instant-speed casting).",

        "Flying and Flash (evasive; castable as an instant).",

        "Flying, Flash (has flying; may be cast at instant speed).",

    ]
