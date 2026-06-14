from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Deep_Sea_Behemoth.model import Deep_Sea_Behemoth

@bind_card(Deep_Sea_Behemoth)
class Deep_Sea_Behemoth_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, gain control of target creature for as long as you control [CARD_NAME].",

        "When [CARD_NAME] enters play, you gain control of target creature while [CARD_NAME] remains on the battlefield.",

        "As [CARD_NAME] enters the battlefield, take control of target creature for as long as you control [CARD_NAME].",

        "Upon entering the battlefield, [CARD_NAME] lets you gain control of target creature for as long as you control [CARD_NAME].",

        "When [CARD_NAME] arrives, gain control of target creature for as long as [CARD_NAME] is under your control.",

        "When [CARD_NAME] enters the battlefield, seize control of target creature for as long as you control [CARD_NAME].",

        "When [CARD_NAME] enters the battlefield, you control target creature for as long as [CARD_NAME] remains on the battlefield.",

        "When [CARD_NAME] enters the battlefield, take control of target creature for as long as you control [CARD_NAME].",

        "When [CARD_NAME] enters the battlefield, gain control of a target creature for as long as you control [CARD_NAME].",

    ]
