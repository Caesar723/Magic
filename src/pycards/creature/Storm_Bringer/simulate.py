from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Storm_Bringer.model import Storm_Bringer

@bind_card(Storm_Bringer)
class Storm_Bringer_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flying. When [CARD_NAME] enters the battlefield, it deals 3 damage to each opponent and you gain 3 life.",

        "Flying. When [CARD_NAME] enters play, it deals 3 damage to each opponent and you gain 3 life.",

        "Flying. As [CARD_NAME] enters the battlefield, it deals 3 damage to each opponent and you gain 3 life.",

        "Flying. Upon entering the battlefield, [CARD_NAME] deals 3 damage to each opponent and you gain 3 life.",

        "Flying. When [CARD_NAME] arrives, it deals 3 damage to each opponent and you gain 3 life.",

        "Flying. When [CARD_NAME] enters the battlefield, deal 3 damage to each opponent and gain 3 life.",

        "Flying. When [CARD_NAME] enters the battlefield, it deals three damage to each opponent and you gain three life.",

        "Flying. When [CARD_NAME] enters the battlefield, it damages each opponent for 3 and you gain 3 life.",

        "Flying. When [CARD_NAME] enters the battlefield, it deals 3 damage to every opponent and you gain 3 life.",

    ]
