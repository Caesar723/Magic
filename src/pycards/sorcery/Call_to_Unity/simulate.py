from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Call_to_Unity.model import Call_to_Unity

@bind_card(Call_to_Unity)
class Call_to_Unity_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Create two 1/1 white Human creature tokens.",

        "[CARD_NAME] creates a pair of 1/1 white Human creature tokens.",

        "Put two 1/1 white Human creature tokens onto the battlefield.",

        "When you cast [CARD_NAME], create two 1/1 white Human creature tokens.",

        "[CARD_NAME] summons two 1/1 white Human creature tokens.",

        "Create two white Human creature tokens with power and toughness 1/1.",

        "You create two 1/1 white Human tokens.",

        "Generate two 1/1 white Human creature tokens on the battlefield.",

        "[CARD_NAME] places two 1/1 white Human creature tokens into play.",

        "Create two 1/1 Human creature tokens that are white."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_no_creature(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"W": (1, 7)},
            least_mana={"colorless": 1, "W": 1},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
