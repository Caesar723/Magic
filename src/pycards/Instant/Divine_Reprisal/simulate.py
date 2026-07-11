from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Divine_Reprisal.model import Divine_Reprisal

@bind_card(Divine_Reprisal)
class Divine_Reprisal_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Destroy target attacking creature.",
        "[CARD_NAME] destroys target attacking creature.",
        "Choose target attacking creature. Destroy it.",
        "Destroy an attacking creature.",
        "[CARD_NAME] removes target attacking creature from the battlefield.",
        "Target attacking creature is destroyed.",
        "Slay target attacking creature.",
        "Destroy one attacking creature with [CARD_NAME].",
        "[CARD_NAME]: destroy target attacking creature.",
        "Eliminate target attacking creature.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.room.attacker=self.player.opponent.battlefield[0]
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"W":(1,7)},
            least_mana={"colorless":2,"W":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
