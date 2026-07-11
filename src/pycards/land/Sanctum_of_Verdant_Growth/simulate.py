from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Sanctum_of_Verdant_Growth.model import Sanctum_of_Verdant_Growth

@bind_card(Sanctum_of_Verdant_Growth)
class Sanctum_of_Verdant_Growth_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and pay 3 mana to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and pay 3 mana to search your library for a basic Forest and put it onto the battlefield tapped.",

        "When [CARD_NAME] enters the battlefield, it enters tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and pay 3 mana to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "[CARD_NAME] enters tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and pay 3 mana to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "[CARD_NAME] enters the battlefield tapped and produces one green mana. You may tap [CARD_NAME] and pay 3 mana to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and pay 3 mana to find a basic Forest in your library and put it onto the battlefield tapped.",

        "[CARD_NAME] enters tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and pay 3 mana to search your library for a basic Forest card and put that land onto the battlefield tapped.",

        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and pay 3 mana to search your library for a basic Forest and put that card onto the battlefield tapped.",

        "When [CARD_NAME] enters the battlefield tapped, add one green mana to your mana pool. You may tap [CARD_NAME] and pay 3 mana to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and pay 3 mana to search your library for a basic Forest card and put it into play tapped.",
    ]

    @simulate
    def simulate_with_forest_and_search_cost(self):
        # basic_initinal always seeds the library with one card of every basic land,
        # which guarantees that the Forest-search mode has a valid result.
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (0, 3), "B": (0, 3), "G": (0, 3), "R": (0, 3), "W": (0, 3)},
            least_mana={"colorless": 3},
        )

        return self.room.simulate_play(self.card)
