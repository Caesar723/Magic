from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Overgrowth.model import Overgrowth

@bind_card(Overgrowth)
class Overgrowth_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Search your library for a basic land card and put it onto the battlefield tapped. Then shuffle your library. Untap up to one land you control.",

        "[CARD_NAME] lets you search for a basic land, put it onto the battlefield tapped, shuffle, and untap up to one land you control.",

        "Search your library for a basic land card, put it onto the battlefield tapped, shuffle your library, then untap up to one land you control.",

        "[CARD_NAME] searches your library for a basic land, puts it onto the battlefield tapped, shuffles, and untaps up to one land you control.",

        "Find a basic land in your library, put it onto the battlefield tapped, shuffle, then untap up to one land you control.",

        "[CARD_NAME] finds a basic land, puts it onto the battlefield tapped, shuffles your library, and untaps up to one land you control.",

        "Search for a basic land card, put it onto the battlefield tapped, shuffle your library. Untap up to one land you control.",

        "[CARD_NAME] allows you to search for a basic land, put it onto the battlefield tapped, shuffle, and untap up to one land you control.",

        "Search your library for a basic land and put it onto the battlefield tapped. Shuffle. Untap up to one land you control.",

        "[CARD_NAME] searches for a basic land, puts it onto the battlefield tapped, shuffles your library, and untaps up to one land you control."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_initinal_library(self.player, {"land_number": (2, 5)})
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"G": (1, 7)},
            least_mana={"colorless": 1, "G": 1},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
