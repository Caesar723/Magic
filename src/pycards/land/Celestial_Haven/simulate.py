from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Celestial_Haven.model import Celestial_Haven

@bind_card(Celestial_Haven)
class Celestial_Haven_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] enters the battlefield untapped and adds one white mana to your mana pool. Additionally, you may pay 3 life and tap [CARD_NAME] to prevent all combat damage that would be dealt this turn.",

        "[CARD_NAME] enters the battlefield untapped and adds one white mana to your mana pool. You may pay 3 life and tap [CARD_NAME] to prevent all combat damage that would be dealt this turn.",

        "When [CARD_NAME] enters the battlefield, it enters untapped and adds one white mana to your mana pool. You may pay 3 life and tap [CARD_NAME] to prevent all combat damage that would be dealt this turn.",

        "[CARD_NAME] enters untapped and adds one white mana to your mana pool. You may pay 3 life and tap [CARD_NAME] to prevent all combat damage that would be dealt this turn.",

        "[CARD_NAME] enters the battlefield untapped and produces one white mana. You may pay 3 life and tap [CARD_NAME] to prevent all combat damage that would be dealt this turn.",

        "[CARD_NAME] enters the battlefield untapped and adds one white mana to your mana pool. You may pay 3 life and tap [CARD_NAME] to prevent all combat damage that would be dealt for the rest of this turn.",

        "[CARD_NAME] enters untapped and adds one white mana to your mana pool. You may pay 3 life and tap [CARD_NAME] to prevent all combat damage that would be dealt during this turn.",

        "[CARD_NAME] enters the battlefield untapped and adds one white mana to your mana pool. You may pay 3 life and tap [CARD_NAME] to prevent all combat damage that would be dealt this turn to any player or creature.",

        "When [CARD_NAME] enters the battlefield untapped, add one white mana to your mana pool. You may pay 3 life and tap [CARD_NAME] to prevent all combat damage that would be dealt this turn.",

        "[CARD_NAME] enters the battlefield untapped and adds one white mana to your mana pool. You may pay 3 life and tap [CARD_NAME] to prevent all combat damage that would be dealt this turn to creatures and players.",
    ]
