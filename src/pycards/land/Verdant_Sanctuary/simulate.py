from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Verdant_Sanctuary.model import Verdant_Sanctuary

@bind_card(Verdant_Sanctuary)
class Verdant_Sanctuary_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may also tap [CARD_NAME] and deal 3 damage to yourself to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and deal 3 damage to yourself to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "When [CARD_NAME] enters the battlefield, it enters tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and deal 3 damage to yourself to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "[CARD_NAME] enters tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and deal 3 damage to yourself to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "[CARD_NAME] enters the battlefield tapped and produces one green mana. You may tap [CARD_NAME] and deal 3 damage to yourself to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and take 3 damage to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "[CARD_NAME] enters tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and deal 3 damage to yourself to search your library for a basic Forest and put it onto the battlefield tapped.",

        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and deal 3 damage to yourself to find a basic Forest in your library and put it onto the battlefield tapped.",

        "When [CARD_NAME] enters the battlefield tapped, add one green mana to your mana pool. You may tap [CARD_NAME] and deal 3 damage to yourself to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and deal 3 damage to yourself to search your library for a basic Forest card and put that land onto the battlefield tapped.",
    ]
