from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Monk_s_Inner_Rebound.model import Monk_s_Inner_Rebound

@bind_card(Monk_s_Inner_Rebound)
class Monk_s_Inner_Rebound_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter a spell. Redirect its effects back to random object.",
        "[CARD_NAME] counters a spell and redirects its effects to a random object.",
        "Counter target spell and bounce its effects back to a random target.",
        "With [CARD_NAME], counter a spell and redirect its effects randomly.",
        "Counter a spell. Its effects are redirected to a random object.",
        "[CARD_NAME]: counter spell, redirect effects to random object.",
        "Counter one spell and send its effects back at a random object.",
        "Counter a spell and reflect its effects onto a random object.",
        "[CARD_NAME] counters a spell and reflects its effects to a random target.",
        "Counter a spell; redirect its effects to a random object.",
    ]

    @simulate
    def simulate_card_stack(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"W":(3,7)},
            least_mana={"colorless":1,"W":3}
        )

        self.room.env_stack_cards(
            self.player,self.card,preferred_types=("instant","sorcery")
        )
        simulate_info=self.room.simulate_play_in_stack(self.card)
        return simulate_info
