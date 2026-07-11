from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Vampiric_Revelry.model import Vampiric_Revelry

@bind_card(Vampiric_Revelry)
class Vampiric_Revelry_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Randomly destroy a creature. You gain life equal to that creature's toughness.",

        "[CARD_NAME] randomly destroys a creature. You gain life equal to that creature's toughness.",

        "Destroy a creature at random. You gain life equal to its toughness.",

        "[CARD_NAME] destroys a random creature. You gain life equal to that creature's toughness.",

        "A random creature is destroyed. You gain life equal to that creature's toughness.",

        "[CARD_NAME] randomly destroys one creature. You gain life equal to its toughness.",

        "Destroy one creature chosen at random. You gain life equal to that creature's toughness.",

        "[CARD_NAME] destroys a creature at random and you gain life equal to its toughness.",

        "Randomly select a creature and destroy it. You gain life equal to that creature's toughness.",

        "[CARD_NAME] randomly destroys a creature, and you gain life equal to that creature's toughness."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_creature(self.player)
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
