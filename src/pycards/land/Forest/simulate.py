from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Forest.model import Forest

@bind_card(Forest)
class Forest_Simulation(Card_Simulation):

    @simulate
    def simulate_when_enter_landarea(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (0, 4), "B": (0, 4), "G": (0, 4), "R": (0, 4), "W": (0, 4)},
        )

        return self.room.simulate_play(self.card)
