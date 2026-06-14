from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Angelic_Protector.model import Angelic_Protector

@bind_card(Angelic_Protector)
class Angelic_Protector_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you may tap target creature. It doesn't untap during its controller's next untap step.",

        "When [CARD_NAME] enters play, you may tap a target creature. That creature remains tapped through its controller's next untap step.",

        "As [CARD_NAME] enters the battlefield, you may tap target creature. It won't untap during its controller's next untap step.",

        "When [CARD_NAME] arrives on the battlefield, you may tap any target creature. It doesn't untap on its controller's next untap.",

        "Upon entering the battlefield, [CARD_NAME] lets you tap target creature, which stays tapped through the next untap step of its controller.",

        "When [CARD_NAME] enters the battlefield, you may choose a target creature and tap it. It doesn't untap during its controller's next untap step.",

        "When [CARD_NAME] enters the battlefield, you may tap one target creature. That creature skips untapping during its controller's next untap step.",

        "When [CARD_NAME] enters the battlefield, you may tap a creature of your choice. It remains tapped until after its controller's next untap step.",

        "When [CARD_NAME] enters the battlefield, you may tap target creature. It cannot untap during its controller's next untap step.",

    ]
