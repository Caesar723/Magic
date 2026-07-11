from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Forest_s_Embrace.model import Forest_s_Embrace

@bind_card(Forest_s_Embrace)
class Forest_s_Embrace_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Search your library for up to three land cards, put them onto the battlefield tapped, then shuffle your library.",

        "[CARD_NAME] lets you search your library for up to three land cards, put them onto the battlefield tapped, then shuffle.",

        "Search your library for up to three lands, put them onto the battlefield tapped, then shuffle your library.",

        "[CARD_NAME] searches your library for up to three land cards, puts them onto the battlefield tapped, then shuffles.",

        "Find up to three land cards in your library, put them onto the battlefield tapped, then shuffle your library.",

        "[CARD_NAME] finds up to three land cards, puts them onto the battlefield tapped, then shuffles your library.",

        "Search for up to three land cards, put them onto the battlefield tapped, then shuffle your library.",

        "[CARD_NAME] allows you to search for up to three land cards, put them onto the battlefield tapped, and shuffle.",

        "Search your library for up to three land cards and put them onto the battlefield tapped. Shuffle your library.",

        "[CARD_NAME] searches your library for up to three land cards, puts them onto the battlefield tapped, then shuffles your library."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_initinal_library(self.player, {"land_number": (5, 8)})
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"G": (2, 7)},
            least_mana={"colorless": 3, "G": 2},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
