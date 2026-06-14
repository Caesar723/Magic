from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Shadow_Stalker.model import Shadow_Stalker

@bind_card(Shadow_Stalker)
class Shadow_Stalker_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Cannot be targeted by spells or abilities. Whenever [CARD_NAME] attacks, the opponent discards a card.",

        "Can't be targeted by spells or abilities. Whenever [CARD_NAME] attacks, the opponent discards a card.",

        "This can't be targeted by spells or abilities. Whenever [CARD_NAME] attacks, the opponent discards a card.",

        "Hexproof from spells and abilities. Whenever [CARD_NAME] attacks, the opponent discards a card.",

        "Immune to targeting by spells or abilities. Whenever [CARD_NAME] attacks, the opponent discards a card.",

        "Cannot be targeted by spells or abilities. Each time [CARD_NAME] attacks, the opponent discards a card.",

        "Cannot be targeted by spells or abilities. When [CARD_NAME] attacks, the opponent discards a card.",

        "Cannot be targeted by spells or abilities. On attack, [CARD_NAME] makes the opponent discard a card.",

        "Cannot be targeted by spells or abilities. Whenever [CARD_NAME] attacks, your opponent discards a card.",

    ]
