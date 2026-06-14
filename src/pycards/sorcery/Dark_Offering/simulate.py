from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Dark_Offering.model import Dark_Offering

@bind_card(Dark_Offering)
class Dark_Offering_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Your opponent loses 2 life and you gain 2 life.",

        "[CARD_NAME] causes your opponent to lose 2 life and you to gain 2 life.",

        "Each opponent loses 2 life. You gain 2 life.",

        "[CARD_NAME] makes your opponent lose 2 life while you gain 2 life.",

        "Your opponent loses two life. You gain two life.",

        "[CARD_NAME] drains 2 life from your opponent and gives it to you.",

        "Opponent loses 2 life. You gain 2 life.",

        "[CARD_NAME] causes the opponent to lose 2 life and you gain 2 life.",

        "Your opponent loses 2 life. You gain 2 life.",

        "[CARD_NAME] makes your opponent lose 2 life and you gain 2 life."
    ]
