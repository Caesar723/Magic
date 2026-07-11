from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Roar_of_the_Behemoth.model import Roar_of_the_Behemoth

@bind_card(Roar_of_the_Behemoth)
class Roar_of_the_Behemoth_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "All enemy creatures get 0 power until the end of this turn.",
        "[CARD_NAME] sets all enemy creatures to 0 power until end of turn.",
        "Opponent's creatures have 0 power this turn.",
        "All enemy creatures have zero power until end of turn.",
        "[CARD_NAME]: enemy creatures get 0 power until end of turn.",
        "Reduce all enemy creatures' power to 0 until end of turn.",
        "Enemy creatures deal no damage—they have 0 power this turn.",
        "With [CARD_NAME], all opposing creatures have 0 power until end of turn.",
        "All enemy creatures' power becomes 0 until end of turn.",
        "[CARD_NAME] roars, reducing all enemy creatures to 0 power this turn.",
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
            {"G":(2,7)},
            least_mana={"colorless":3,"G":2}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
