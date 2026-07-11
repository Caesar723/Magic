from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Harvest_Blessing.model import Harvest_Blessing

@bind_card(Harvest_Blessing)
class Harvest_Blessing_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Search your library for a basic land card, put it onto the battlefield tapped, then shuffle your library. Target creature you control gets +1/+1 until end of turn.",

        "[CARD_NAME] lets you search for a basic land, put it onto the battlefield tapped, shuffle, and give target creature you control +1/+1 until end of turn.",

        "Search your library for a basic land, put it onto the battlefield tapped, shuffle your library. Target creature you control gets +1/+1 until end of turn.",

        "[CARD_NAME] searches your library for a basic land, puts it onto the battlefield tapped, shuffles, and buffs target creature you control with +1/+1 until end of turn.",

        "Find a basic land in your library, put it onto the battlefield tapped, shuffle, then target creature you control gets +1/+1 until end of turn.",

        "[CARD_NAME] finds a basic land, puts it onto the battlefield tapped, shuffles your library, and gives target creature you control +1/+1 until end of turn.",

        "Search for a basic land card, put it onto the battlefield tapped, shuffle your library. A target creature you control gets +1/+1 until end of turn.",

        "[CARD_NAME] allows you to search for a basic land, put it onto the battlefield tapped, shuffle, and grant +1/+1 to target creature you control until end of turn.",

        "Search your library for a basic land and put it onto the battlefield tapped. Shuffle. Target creature you control gets +1/+1 until end of turn.",

        "[CARD_NAME] searches for a basic land, puts it onto the battlefield tapped, shuffles your library, and target creature you control gets +1/+1 until end of turn."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_initinal_library(self.player, {"land_number": (2, 5)})
        self.room.env_creature(self.player)
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
