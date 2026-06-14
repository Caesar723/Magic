from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Aetheric_Nexus.model import Aetheric_Nexus

@bind_card(Aetheric_Nexus)
class Aetheric_Nexus_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] enters the battlefield untapped and adds one colorless mana to your mana pool. You may also tap [CARD_NAME] to add one mana of any color, but only if you control a creature.",

        "[CARD_NAME] enters the battlefield untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color if you control a creature.",

        "When [CARD_NAME] enters the battlefield, it enters untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color, but only if you control a creature.",

        "[CARD_NAME] enters untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color if you control a creature.",

        "[CARD_NAME] enters the battlefield untapped and produces one colorless mana. You may tap [CARD_NAME] to add one mana of any color, but only if you control a creature.",

        "[CARD_NAME] enters the battlefield untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color while you control a creature.",

        "[CARD_NAME] enters untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color, but only if you have a creature on the battlefield.",

        "[CARD_NAME] enters the battlefield untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color if you have at least one creature.",

        "When [CARD_NAME] enters the battlefield untapped, add one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color, but only if you control a creature.",

        "[CARD_NAME] enters the battlefield untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color, but only if you control at least one creature.",
    ]
