from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Soul_Siphon.model import Soul_Siphon

@bind_card(Soul_Siphon)
class Soul_Siphon_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Randomly destroy an opponent's creature. You gain life equal to that creature's power.",

        "[CARD_NAME] randomly destroys an opponent's creature. You gain life equal to that creature's power.",

        "Destroy a random creature controlled by an opponent. You gain life equal to its power.",

        "[CARD_NAME] destroys a random opponent's creature. You gain life equal to that creature's power.",

        "An opponent's creature is destroyed at random. You gain life equal to that creature's power.",

        "[CARD_NAME] randomly destroys one of an opponent's creatures. You gain life equal to its power.",

        "Destroy one of an opponent's creatures chosen at random. You gain life equal to that creature's power.",

        "[CARD_NAME] destroys an opponent's creature at random and you gain life equal to its power.",

        "Randomly select an opponent's creature and destroy it. You gain life equal to that creature's power.",

        "[CARD_NAME] randomly destroys an opponent's creature, and you gain life equal to that creature's power."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.room.env_life_low(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"B": (1, 7)},
            least_mana={"colorless": 1, "B": 1},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
