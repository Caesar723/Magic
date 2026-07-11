from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Judgment_Day.model import Judgment_Day

@bind_card(Judgment_Day)
class Judgment_Day_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Destroy all creatures. Then, each player may return one creature card from their graveyard to the battlefield.",

        "[CARD_NAME] destroys all creatures. Then each player may return one creature card from their graveyard to the battlefield.",

        "Destroy every creature. Then each player may return a creature card from their graveyard to the battlefield.",

        "[CARD_NAME] wipes all creatures. Then each player may return one creature card from their graveyard to the battlefield.",

        "All creatures are destroyed. Then each player may return one creature card from their graveyard to the battlefield.",

        "[CARD_NAME] destroys all creatures on the battlefield. Then each player may return one creature card from their graveyard.",

        "Destroy all creatures. Afterward, each player may return one creature card from their graveyard to the battlefield.",

        "[CARD_NAME] destroys every creature. Then each player may put one creature card from their graveyard onto the battlefield.",

        "All creatures die. Then each player may return one creature card from their graveyard to the battlefield.",

        "[CARD_NAME] destroys all creatures. Then each player may return a creature card from their graveyard to the battlefield."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_initinal_graveyard(self.player, {"creature_number": (2, 5)})
        self.room.env_initinal_graveyard(self.player.opponent, {"creature_number": (2, 5)})
        self.room.env_creature(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"W": (2, 7)},
            least_mana={"colorless": 3, "W": 2},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
