from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Time_Warp.model import Time_Warp

@bind_card(Time_Warp)
class Time_Warp_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] allows you to take an extra turn after this one. You skip the untap step of that turn.",
        "[CARD_NAME] grants an extra turn after this one; you skip the untap step of that turn.",
        "Take an extra turn after this one. Skip untap step on that turn.",
        "Extra turn after this one. No untap step on the extra turn.",
        "[CARD_NAME]: extra turn, skip untap on that turn.",
        "Gain an additional turn; skip untap during it.",
        "With [CARD_NAME], take another turn and skip untap on that turn.",
        "An extra turn after this one without an untap step.",
        "[CARD_NAME] gives extra turn; untap step is skipped.",
        "Take extra turn after this one, skipping untap step.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U":(2,7)},
            least_mana={"colorless":3,"U":2}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
