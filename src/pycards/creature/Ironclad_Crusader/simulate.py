from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Ironclad_Crusader.model import Ironclad_Crusader

@bind_card(Ironclad_Crusader)
class Ironclad_Crusader_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you may tap target creature an opponent controls. That creature doesn't untap during its controller's next untap step.",

        "When [CARD_NAME] enters play, you may tap target creature an opponent controls. It doesn't untap during its controller's next untap step.",

        "As [CARD_NAME] enters the battlefield, you may tap target creature an opponent controls. It won't untap during its controller's next untap step.",

        "Upon entering the battlefield, [CARD_NAME] lets you tap target creature an opponent controls. It doesn't untap during its controller's next untap step.",

        "When [CARD_NAME] arrives, you may tap target creature an opponent controls. It doesn't untap during its controller's next untap step.",

        "When [CARD_NAME] enters the battlefield, you may tap an opposing creature. It doesn't untap during its controller's next untap step.",

        "When [CARD_NAME] enters the battlefield, you may tap target creature an opponent controls. That creature skips untapping during its controller's next untap step.",

        "When [CARD_NAME] enters the battlefield, you may tap a target creature an opponent controls. It doesn't untap during its controller's next untap step.",

        "When [CARD_NAME] enters the battlefield, you may tap target opposing creature. It doesn't untap during its controller's next untap step.",

    ]
