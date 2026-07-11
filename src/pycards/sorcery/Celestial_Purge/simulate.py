from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Celestial_Purge.model import Celestial_Purge

@bind_card(Celestial_Purge)
class Celestial_Purge_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Exile target black or red permanent.",

        "[CARD_NAME] exiles target black or red permanent.",

        "Exile a target permanent that is black or red.",

        "[CARD_NAME] exiles one target permanent if it is black or red.",

        "Choose target black or red permanent. Exile it.",

        "[CARD_NAME] removes target black or red permanent from the game by exiling it.",

        "Target black or red permanent is exiled.",

        "[CARD_NAME] exiles a chosen target permanent that is either black or red.",

        "Exile one target permanent that is black or red.",

        "[CARD_NAME] causes target black or red permanent to be exiled."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.room.env_one_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"W": (1, 7)},
            least_mana={"colorless": 2, "W": 1},
        )

        self.player.opponent.battlefield[0].color = "red"

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
