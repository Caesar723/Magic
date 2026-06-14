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

        "Flash, Flying.",

        "Flash. Flying.",

        "Flash (cast at instant speed) and Flying.",

        "Flash (you may cast this any time you could cast an instant) and Flying.",

        "Flash and Flying (can be cast at instant speed and can't be blocked except by flying or reach).",

        "Flash, Flying (instant-speed casting and evasion).",

        "Flash and Flying (castable as an instant; evasive).",

        "Flash and Flying (may be cast at instant speed; has flying).",

    ]
