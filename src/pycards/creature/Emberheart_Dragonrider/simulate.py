from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Emberheart_Dragonrider.model import Emberheart_Dragonrider

@bind_card(Emberheart_Dragonrider)
class Emberheart_Dragonrider_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you may pay R. If you do, target creature gains haste until end of turn.",

        "When [CARD_NAME] enters play, you may pay R. If you do, target creature gains haste until end of turn.",

        "As [CARD_NAME] enters the battlefield, you may pay R. If you do, target creature gains haste until end of turn.",

        "Upon entering the battlefield, [CARD_NAME] lets you pay R to give target creature haste until end of turn.",

        "When [CARD_NAME] arrives, you may pay R. If you do, target creature gains haste until end of turn.",

        "When [CARD_NAME] enters the battlefield, you may spend R. If you do, target creature gains haste until end of turn.",

        "When [CARD_NAME] enters the battlefield, you may pay one red mana. If you do, target creature gains haste until end of turn.",

        "When [CARD_NAME] enters the battlefield, you may pay R. If you do, a target creature gains haste until end of turn.",

        "When [CARD_NAME] enters the battlefield, you may pay R. If you do, target creature has haste until end of turn.",

    ]
