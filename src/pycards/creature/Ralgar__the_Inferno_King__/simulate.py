from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Ralgar__the_Inferno_King__.model import Ralgar__the_Inferno_King__

@bind_card(Ralgar__the_Inferno_King__)
class Ralgar__the_Inferno_King___Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, it deals 3 damage to any target. Whenever you cast an instant or sorcery spell, [CARD_NAME] gets +1/+0 until end of turn.",

        "When [CARD_NAME] enters play, it deals 3 damage to any target. Whenever you cast an instant or sorcery, [CARD_NAME] gets +1/+0 until end of turn.",

        "As [CARD_NAME] enters the battlefield, it deals 3 damage to any target. Whenever you cast an instant or sorcery spell, [CARD_NAME] gets +1/+0 until end of turn.",

        "Upon entering the battlefield, [CARD_NAME] deals 3 damage to any target. Whenever you cast an instant or sorcery spell, [CARD_NAME] gets +1/+0 until end of turn.",

        "When [CARD_NAME] arrives, it deals 3 damage to any target. Whenever you cast an instant or sorcery spell, [CARD_NAME] gets +1/+0 until end of turn.",

        "When [CARD_NAME] enters the battlefield, deal 3 damage to any target. Whenever you cast an instant or sorcery spell, [CARD_NAME] gets +1/+0 until end of turn.",

        "When [CARD_NAME] enters the battlefield, it deals three damage to any target. Whenever you cast an instant or sorcery spell, [CARD_NAME] gets +1/+0 until end of turn.",

        "When [CARD_NAME] enters the battlefield, it deals 3 damage to any target. Each time you cast an instant or sorcery spell, [CARD_NAME] gets +1/+0 until end of turn.",

        "When [CARD_NAME] enters the battlefield, it deals 3 damage to any target. When you cast an instant or sorcery spell, [CARD_NAME] gets +1/+0 until end of turn.",

    ]
