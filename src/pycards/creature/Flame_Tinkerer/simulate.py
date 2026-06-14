from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Flame_Tinkerer.model import Flame_Tinkerer

@bind_card(Flame_Tinkerer)
class Flame_Tinkerer_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you may pay R. If you do, it deals 1 damage to target creature.",

        "When [CARD_NAME] enters play, you may pay R. If you do, it deals 1 damage to target creature.",

        "As [CARD_NAME] enters the battlefield, you may pay R. If you do, it deals 1 damage to target creature.",

        "Upon entering the battlefield, [CARD_NAME] lets you pay R to deal 1 damage to target creature.",

        "When [CARD_NAME] arrives, you may pay R. If you do, it deals 1 damage to target creature.",

        "When [CARD_NAME] enters the battlefield, you may spend R. If you do, it deals 1 damage to target creature.",

        "When [CARD_NAME] enters the battlefield, you may pay one red mana. If you do, it deals 1 damage to target creature.",

        "When [CARD_NAME] enters the battlefield, you may pay R. If you do, it deals one damage to target creature.",

        "When [CARD_NAME] enters the battlefield, you may pay R. If you do, deal 1 damage to target creature.",

    ]
