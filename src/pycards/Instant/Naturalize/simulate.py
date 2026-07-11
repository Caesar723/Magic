from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Naturalize.model import Naturalize

@bind_card(Naturalize)
class Naturalize_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Destroy target creature.",
        "[CARD_NAME] destroys target creature.",
        "Choose target creature. Destroy it.",
        "Destroy a creature.",
        "[CARD_NAME] removes target creature from the battlefield.",
        "Target creature is destroyed.",
        "Slay target creature with [CARD_NAME].",
        "Eliminate target creature.",
        "[CARD_NAME]: destroy target creature.",
        "Destroy one creature.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"G":(1,7)},
            least_mana={"colorless":3,"G":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
