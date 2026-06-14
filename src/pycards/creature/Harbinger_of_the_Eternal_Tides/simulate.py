from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Harbinger_of_the_Eternal_Tides.model import Harbinger_of_the_Eternal_Tides

@bind_card(Harbinger_of_the_Eternal_Tides)
class Harbinger_of_the_Eternal_Tides_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flash. When [CARD_NAME] enters the battlefield, tap target creature an opponent controls. It doesn't untap during its controller's next untap step.",

        "Flash. When [CARD_NAME] enters play, tap target creature an opponent controls. It doesn't untap during its controller's next untap step.",

        "Flash. As [CARD_NAME] enters the battlefield, tap target creature an opponent controls. It won't untap during its controller's next untap step.",

        "Flash. Upon entering the battlefield, [CARD_NAME] taps target creature an opponent controls. It doesn't untap during its controller's next untap step.",

        "Flash. When [CARD_NAME] arrives, tap target creature an opponent controls. It doesn't untap during its controller's next untap step.",

        "Flash. When [CARD_NAME] enters the battlefield, tap an opposing creature. It doesn't untap during its controller's next untap step.",

        "Flash. When [CARD_NAME] enters the battlefield, tap target creature an opponent controls. That creature skips untapping during its controller's next untap step.",

        "Flash. When [CARD_NAME] enters the battlefield, tap a target creature an opponent controls. It doesn't untap during its controller's next untap step.",

        "Flash. When [CARD_NAME] enters the battlefield, tap target opposing creature. It doesn't untap during its controller's next untap step.",

    ]
