from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Wild_Growth.model import Wild_Growth

@bind_card(Wild_Growth)
class Wild_Growth_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Search your library for a basic land card and put it onto the battlefield tapped, then shuffle your library.",
        "[CARD_NAME] searches for a basic land, puts it tapped onto the battlefield, and shuffles.",
        "Find a basic land in your library, play it tapped, shuffle.",
        "Tutor basic land to battlefield tapped. Shuffle library.",
        "[CARD_NAME]: basic land to battlefield tapped.",
        "Search library for basic land, put in play tapped, shuffle.",
        "With [CARD_NAME], fetch a tapped basic land from your library.",
        "Put a basic land from library onto battlefield tapped. Shuffle.",
        "Basic land search, enter tapped, shuffle.",
        "[CARD_NAME] ramps with a tapped basic land from library.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"G":(1,7)},
            least_mana={"colorless":1,"G":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
