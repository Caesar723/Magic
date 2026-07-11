from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Temporal_Distortion.model import Temporal_Distortion

@bind_card(Temporal_Distortion)
class Temporal_Distortion_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] allows you to take an extra turn after this one. Exile [CARD_NAME].",

        "Take an extra turn after this one. Exile [CARD_NAME].",

        "[CARD_NAME] grants you an extra turn after this one, then exiles itself.",

        "You take an extra turn after this one. Exile [CARD_NAME].",

        "[CARD_NAME] lets you take an additional turn after this one. Exile [CARD_NAME].",

        "Take one extra turn after this one. Exile [CARD_NAME].",

        "[CARD_NAME] gives you an extra turn after this one. Exile [CARD_NAME].",

        "After this turn, take an extra turn. Exile [CARD_NAME].",

        "[CARD_NAME] allows an extra turn after this one. Exile [CARD_NAME].",

        "You get an extra turn after this one. Exile [CARD_NAME]."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (2, 7)},
            least_mana={"colorless": 3, "U": 2},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
