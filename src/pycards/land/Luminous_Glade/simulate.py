from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Luminous_Glade.model import Luminous_Glade

@bind_card(Luminous_Glade)
class Luminous_Glade_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] enters the battlefield tapped and adds one white mana to your mana pool. You may tap [CARD_NAME] to prevent the next 1 damage that would be dealt to target creature or player this turn.",

        "[CARD_NAME] enters the battlefield tapped and adds one white mana to your mana pool. You may tap [CARD_NAME] to prevent the next 1 damage that would be dealt to a creature or player this turn.",

        "When [CARD_NAME] enters the battlefield, it enters tapped and adds one white mana to your mana pool. You may tap [CARD_NAME] to prevent the next 1 damage that would be dealt to target creature or player this turn.",

        "[CARD_NAME] enters tapped and adds one white mana to your mana pool. You may tap [CARD_NAME] to prevent the next 1 damage that would be dealt to a target creature or player this turn.",

        "[CARD_NAME] enters the battlefield tapped and produces one white mana. You may tap [CARD_NAME] to prevent the next 1 damage that would be dealt to target creature or player this turn.",

        "[CARD_NAME] enters the battlefield tapped and adds one white mana to your mana pool. You may tap [CARD_NAME] to prevent the next point of damage that would be dealt to target creature or player this turn.",

        "[CARD_NAME] enters tapped and adds one white mana to your mana pool. You may tap [CARD_NAME] to prevent the next 1 damage that would be dealt to a chosen creature or player this turn.",

        "[CARD_NAME] enters the battlefield tapped and adds one white mana to your mana pool. You may tap [CARD_NAME] to prevent the next 1 damage that would be dealt to a creature or player of your choice this turn.",

        "When [CARD_NAME] enters the battlefield tapped, add one white mana to your mana pool. You may tap [CARD_NAME] to prevent the next 1 damage that would be dealt to target creature or player this turn.",

        "[CARD_NAME] enters the battlefield tapped and adds one white mana to your mana pool. You may tap [CARD_NAME] to prevent the next 1 damage that would be dealt to a target creature or player this turn.",
    ]
