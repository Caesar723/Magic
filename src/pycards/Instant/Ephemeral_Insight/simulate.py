from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Ephemeral_Insight.model import Ephemeral_Insight

@bind_card(Ephemeral_Insight)
class Ephemeral_Insight_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Scry 2, then draw a card. Put this card to your hand again.",
        "[CARD_NAME] lets you scry 2, draw a card, then returns itself to your hand.",
        "Scry 2, draw a card, then put [CARD_NAME] back into your hand.",
        "Look at the top two cards of your library, draw a card, then return [CARD_NAME] to your hand.",
        "Scry 2, then draw. [CARD_NAME] goes back to your hand.",
        "[CARD_NAME]: scry 2, draw a card, return this card to hand.",
        "Scry two, draw one, then put this spell back in your hand.",
        "With [CARD_NAME], scry 2, draw a card, and return it to your hand.",
        "Scry 2 and draw a card. Return [CARD_NAME] to your hand.",
        "Scry 2, draw a card, then [CARD_NAME] returns to your hand.",
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
            {"U":(1,7)},
            least_mana={"colorless":1,"U":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
