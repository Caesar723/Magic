from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Celestial_Skyweaver.model import Celestial_Skyweaver

@bind_card(Celestial_Skyweaver)
class Celestial_Skyweaver_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flying. Whenever you cast an instant or sorcery spell, you may tap target creature an opponent controls.",

        "Flying. Each time you cast an instant or sorcery, you may tap target creature an opponent controls.",

        "Flying. Whenever you play an instant or sorcery spell, you may tap a target creature an opponent controls.",

        "Flying. When you cast an instant or sorcery spell, you may tap target creature an opponent controls.",

        "Flying. Whenever you cast an instant or sorcery, you may tap an opposing creature of your choice.",

        "Flying. Each instant or sorcery you cast lets you tap target creature an opponent controls.",

        "Flying. Whenever you cast an instant or sorcery spell, you may tap one target creature an opponent controls.",

        "Flying. On casting an instant or sorcery, you may tap target creature an opponent controls.",

        "Flying. Whenever you cast an instant or sorcery spell, you may tap a target opposing creature.",

    ]
