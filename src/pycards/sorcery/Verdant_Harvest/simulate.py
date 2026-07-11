from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Verdant_Harvest.model import Verdant_Harvest

@bind_card(Verdant_Harvest)
class Verdant_Harvest_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Search your library for a basic land card and put it onto the battlefield tapped, then shuffle your library. Draw a card.",

        "[CARD_NAME] lets you search your library for a basic land, put it onto the battlefield tapped, shuffle, then draw a card.",

        "Search your library for a basic land card, put it onto the battlefield tapped, shuffle your library, and draw a card.",

        "[CARD_NAME] searches your library for a basic land, puts it onto the battlefield tapped, shuffles, then you draw a card.",

        "Find a basic land card in your library, put it onto the battlefield tapped, shuffle, then draw a card.",

        "[CARD_NAME] allows you to search for a basic land, put it onto the battlefield tapped, shuffle your library, and draw a card.",

        "Search your library for a basic land and put it onto the battlefield tapped. Shuffle your library. Draw a card.",

        "[CARD_NAME] finds a basic land in your library, puts it onto the battlefield tapped, shuffles, and draws you a card.",

        "Search for a basic land card, put it onto the battlefield tapped, shuffle your library, then draw one card.",

        "[CARD_NAME] searches your library for a basic land card, puts it onto the battlefield tapped, shuffles, then draws a card."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_initinal_library(self.player, {"land_number": (2, 5), "creature_number": (1, 3)})
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"G": (2, 7)},
            least_mana={"colorless": 1, "G": 2},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
