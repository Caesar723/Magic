from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Mystic_Reflection_Pool.model import Mystic_Reflection_Pool

@bind_card(Mystic_Reflection_Pool)
class Mystic_Reflection_Pool_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] enters the battlefield untapped and adds one blue mana to your mana pool. Additionally, you may tap [CARD_NAME] and pay 1 mana to scry 2, then draw a card.",

        "[CARD_NAME] enters the battlefield untapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] and pay 1 mana to scry 2, then draw a card.",

        "When [CARD_NAME] enters the battlefield, it enters untapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] and pay 1 mana to scry 2, then draw a card.",

        "[CARD_NAME] enters untapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] and pay 1 mana to scry 2, then draw a card.",

        "[CARD_NAME] enters the battlefield untapped and produces one blue mana. You may tap [CARD_NAME] and pay 1 mana to scry 2, then draw a card.",

        "[CARD_NAME] enters the battlefield untapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] and pay 1 mana to scry 2 and draw a card.",

        "[CARD_NAME] enters untapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] and pay 1 mana to scry two, then draw a card.",

        "[CARD_NAME] enters the battlefield untapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] and pay 1 mana to look at the top two cards of your library, then draw a card.",

        "When [CARD_NAME] enters the battlefield untapped, add one blue mana to your mana pool. You may tap [CARD_NAME] and pay 1 mana to scry 2, then draw a card.",

        "[CARD_NAME] enters the battlefield untapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] and pay 1 mana to scry 2, then draw one card.",
    ]
