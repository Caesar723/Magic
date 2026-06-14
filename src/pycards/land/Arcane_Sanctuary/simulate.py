from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Arcane_Sanctuary.model import Arcane_Sanctuary

@bind_card(Arcane_Sanctuary)
class Arcane_Sanctuary_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] enters the battlefield tapped and adds one colorless mana to your mana pool. You may also tap [CARD_NAME] and pay 2 mana to scry 2 and draw a card.",

        "[CARD_NAME] enters the battlefield tapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to scry 2, then draw a card.",

        "When [CARD_NAME] enters the battlefield, it enters tapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to scry 2 and draw a card.",

        "[CARD_NAME] enters tapped and produces one colorless mana. You may tap [CARD_NAME] and pay 2 mana to scry 2 and draw a card.",

        "[CARD_NAME] enters the battlefield tapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to look at the top two cards of your library, then draw a card.",

        "[CARD_NAME] enters the battlefield tapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to scry 2, then draw one card.",

        "[CARD_NAME] enters tapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to scry 2 and draw a card.",

        "[CARD_NAME] enters the battlefield tapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to scry two, then draw a card.",

        "When [CARD_NAME] enters the battlefield tapped, add one colorless mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to scry 2 and draw a card.",

        "[CARD_NAME] enters the battlefield tapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to scry 2 and draw one card.",
    ]
