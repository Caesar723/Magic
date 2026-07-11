from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Unearthly_Blaze.model import Unearthly_Blaze

@bind_card(Unearthly_Blaze)
class Unearthly_Blaze_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 3 damage to any target.",

        "Deal 3 damage to any target.",

        "[CARD_NAME] deals three damage to any target.",

        "Deal three damage to any target.",

        "[CARD_NAME] inflicts 3 damage on any target.",

        "Any target takes 3 damage.",

        "[CARD_NAME] hits any target for 3 damage.",

        "Deal 3 damage to a target of your choice.",

        "[CARD_NAME] deals 3 damage to a chosen target.",

        "Choose any target. [CARD_NAME] deals 3 damage to it."
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
            {"R": (2, 7)},
            least_mana={"colorless": 1, "R": 2},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
