from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Arcane_Intervention.model import Arcane_Intervention

@bind_card(Arcane_Intervention)
class Arcane_Intervention_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Return target permanent to its owner's hand. Draw a card.",
        "[CARD_NAME] bounces target permanent to its owner's hand, then you draw a card.",
        "Choose target permanent. Return it to its owner's hand. Draw a card.",
        "Send target permanent back to its owner's hand. Draw a card.",
        "[CARD_NAME] returns a permanent to hand and lets you draw a card.",
        "Return target permanent to its owner's hand, then draw a card.",
        "Bounce target permanent. Draw a card.",
        "[CARD_NAME]: return a permanent to hand, draw a card.",
        "Target permanent returns to its owner's hand. You draw a card.",
        "Return one permanent to its owner's hand, then draw a card with [CARD_NAME].",
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
            {"U":(2,7)},
            least_mana={"colorless":1,"U":2}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
