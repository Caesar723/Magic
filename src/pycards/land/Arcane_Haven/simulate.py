from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Arcane_Haven.model import Arcane_Haven

@bind_card(Arcane_Haven)
class Arcane_Haven_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] enters the battlefield untapped and adds one colorless mana to your mana pool. You may also tap [CARD_NAME] to add one mana of any color to your mana pool if your's life above 10.",

        "[CARD_NAME] enters the battlefield untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color to your mana pool if your life is above 10.",

        "When [CARD_NAME] enters the battlefield, it enters untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color to your mana pool if your life is above 10.",

        "[CARD_NAME] enters untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color to your mana pool if your life is above 10.",

        "[CARD_NAME] enters the battlefield untapped and produces one colorless mana. You may tap [CARD_NAME] to add one mana of any color to your mana pool if your life is above 10.",

        "[CARD_NAME] enters the battlefield untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color to your mana pool while your life total is above 10.",

        "[CARD_NAME] enters untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color to your mana pool if you have more than 10 life.",

        "[CARD_NAME] enters the battlefield untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color to your mana pool if your life total is greater than 10.",

        "When [CARD_NAME] enters the battlefield untapped, add one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color to your mana pool if your life is above 10.",

        "[CARD_NAME] enters the battlefield untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color to your mana pool if your life total is above 10.",
    ]
