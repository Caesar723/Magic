from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Nyxborn_Serpent.model import Nyxborn_Serpent

@bind_card(Nyxborn_Serpent)
class Nyxborn_Serpent_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Constellation — Whenever [CARD_NAME] enters the battlefield under your control, you may tap target creature an opponent controls.",

        "Constellation — When [CARD_NAME] enters the battlefield under your control, you may tap target creature an opponent controls.",

        "Constellation — As [CARD_NAME] enters the battlefield under your control, you may tap target creature an opponent controls.",

        "Constellation — Upon entering under your control, [CARD_NAME] lets you tap target creature an opponent controls.",

        "Constellation — When [CARD_NAME] enters under your control, you may tap target creature an opponent controls.",

        "Constellation — Whenever [CARD_NAME] enters the battlefield under your control, you may tap an opposing creature.",

        "Constellation — Whenever [CARD_NAME] enters under your control, you may tap target creature an opponent controls.",

        "Constellation — Whenever [CARD_NAME] enters the battlefield under your control, you may tap a target creature an opponent controls.",

        "Constellation — Whenever [CARD_NAME] enters the battlefield under your control, you may tap target opposing creature.",

    ]
