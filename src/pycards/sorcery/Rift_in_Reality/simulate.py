from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Rift_in_Reality.model import Rift_in_Reality

@bind_card(Rift_in_Reality)
class Rift_in_Reality_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] allows you to exile target creature. Return it to the battlefield under its owner's control at the beginning of the next end step. When it returns, its owner draws a card.",

        "Exile target creature. Return it to the battlefield under its owner's control at the beginning of the next end step. When it returns, its owner draws a card.",

        "[CARD_NAME] exiles target creature, then returns it to the battlefield under its owner's control at the next end step. Its owner draws a card when it returns.",

        "Exile a target creature. At the beginning of the next end step, return it to the battlefield under its owner's control. When it returns, its owner draws a card.",

        "[CARD_NAME] exiles target creature temporarily. It returns to the battlefield under its owner's control at the beginning of the next end step, and its owner draws a card.",

        "Exile target creature. Return it under its owner's control at the beginning of the next end step. When it returns, its owner draws a card.",

        "[CARD_NAME] removes target creature from the game, then returns it to the battlefield under its owner's control at the next end step. Its owner draws a card.",

        "Exile target creature. At the beginning of the next end step, put it onto the battlefield under its owner's control. When it returns, its owner draws a card.",

        "[CARD_NAME] exiles target creature and returns it to the battlefield under its owner's control at the beginning of the next end step. Its owner draws a card when it returns.",

        "Exile target creature. Return it to the battlefield under its owner's control at the beginning of the next end step. Its owner draws a card when it returns."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (1, 7)},
            least_mana={"colorless": 1, "U": 1},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
