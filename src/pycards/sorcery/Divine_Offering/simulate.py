from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Divine_Offering.model import Divine_Offering

@bind_card(Divine_Offering)
class Divine_Offering_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Destroy target land. Its controller gains 3 life.",

        "[CARD_NAME] destroys target land. Its controller gains 3 life.",

        "Destroy a target land. That land's controller gains 3 life.",

        "[CARD_NAME] destroys target land and its controller gains 3 life.",

        "Choose target land. Destroy it. Its controller gains 3 life.",

        "[CARD_NAME] destroys a chosen target land. Its controller gains 3 life.",

        "Target land is destroyed. Its controller gains 3 life.",

        "[CARD_NAME] destroys target land, and its controller gains three life.",

        "Destroy one target land. Its controller gains 3 life.",

        "[CARD_NAME] causes target land to be destroyed. Its controller gains 3 life."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.room.env_life_low(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"W": (1, 7)},
            least_mana={"colorless": 2, "W": 1},
        )

        self.room.env_mana(self.player.opponent, {"W": (1, 4)})

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
