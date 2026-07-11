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

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.room.env_life_low(self.player)
        self.random_env_creature()(self.player.opponent)
        self.room.env_life_middle(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"B": (1, 7)},
            least_mana={"colorless": 1, "B": 1},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
