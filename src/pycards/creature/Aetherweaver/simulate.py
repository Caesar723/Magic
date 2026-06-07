from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation
from pycards.creature.Aetherweaver.model import Aetherweaver

@bind_card(Aetherweaver)
class Aetherweaver_Simulation(Card_Simulation):
    
    @simulate
    def simulate_when_enter_battlefield(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U":(1,7)},
            least_mana={"colorless":2,"U":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
        