from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mystical_Barrier.model import Mystical_Barrier

@bind_card(Mystical_Barrier)
class Mystical_Barrier_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell. If [CARD_NAME] is countered this way, you may draw a card.",
        "[CARD_NAME] counters target spell; you may draw a card if it is countered this way.",
        "Counter a spell. If countered this way, you may draw a card.",
        "With [CARD_NAME], counter target spell and optionally draw if countered.",
        "Counter target spell. On counter, you may draw a card.",
        "[CARD_NAME]: counter spell; optional draw when countered.",
        "Counter target spell. Draw a card if [CARD_NAME] counters it this way.",
        "Counter a spell. If countered by [CARD_NAME], you may draw.",
        "[CARD_NAME] counters target spell; draw optional on successful counter.",
        "Counter target spell. You may draw if countered this way.",
    ]

    @simulate
    def simulate_card_stack(self):
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

        self.room.env_stack_cards(self.player,self.card)
        simulate_info=self.room.simulate_play_in_stack(self.card)
        return simulate_info
