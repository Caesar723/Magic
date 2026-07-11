from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Fiery_Blast.model import Fiery_Blast

@bind_card(Fiery_Blast)
class Fiery_Blast_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 2 damage to any target.",
        "Deal 2 damage to any target.",
        "[CARD_NAME] hits any target for 2 damage.",
        "Choose any target. Deal 2 damage.",
        "Fire 2 damage at any target with [CARD_NAME].",
        "[CARD_NAME] inflicts 2 damage on any target.",
        "Any target takes 2 damage.",
        "Deal two damage to any target.",
        "[CARD_NAME] strikes any target for 2.",
        "Target anything; deal 2 damage.",
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
            {"R":(1,7)},
            least_mana={"colorless":1,"R":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
