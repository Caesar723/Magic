from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Volcanic_Fumaroles.model import Volcanic_Fumaroles

@bind_card(Volcanic_Fumaroles)
class Volcanic_Fumaroles_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] enters the battlefield tapped and adds one red mana to your mana pool. You mayp pay 1 mana to tap [CARD_NAME] and deal 1 damage to random opponent's creature or player.",

        "[CARD_NAME] enters the battlefield tapped and adds one red mana to your mana pool. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random opponent's creature or player.",

        "When [CARD_NAME] enters the battlefield, it enters tapped and adds one red mana to your mana pool. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random opponent's creature or player.",

        "[CARD_NAME] enters tapped and adds one red mana to your mana pool. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random creature or player controlled by an opponent.",

        "[CARD_NAME] enters the battlefield tapped and produces one red mana. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random opponent's creature or player.",

        "[CARD_NAME] enters the battlefield tapped and adds one red mana to your mana pool. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random opponent creature or the opponent.",

        "[CARD_NAME] enters tapped and adds one red mana to your mana pool. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random target among an opponent's creatures and that opponent.",

        "[CARD_NAME] enters the battlefield tapped and adds one red mana to your mana pool. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random creature or player an opponent controls.",

        "When [CARD_NAME] enters the battlefield tapped, add one red mana to your mana pool. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random opponent's creature or player.",

        "[CARD_NAME] enters the battlefield tapped and adds one red mana to your mana pool. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random opponent's creature or to the opponent.",
    ]
