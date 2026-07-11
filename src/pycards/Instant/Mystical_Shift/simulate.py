from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mystical_Shift.model import Mystical_Shift

@bind_card(Mystical_Shift)
class Mystical_Shift_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell and draw a card unless its controller's mana pool is less than 3.",
        "[CARD_NAME] counters target spell and draws a card unless controller has less than 3 mana.",
        "Counter a spell and draw unless controller's mana pool is under 3.",
        "With [CARD_NAME], counter and draw unless controller has fewer than 3 mana.",
        "Counter target spell, draw a card unless controller's mana is below 3.",
        "[CARD_NAME]: counter + draw unless mana pool <3.",
        "Counter and draw unless controller has at least 3 mana.",
        "Counter target spell. You draw unless controller's mana pool is less than 3.",
        "[CARD_NAME] counters and draws unless controller can pay from 3+ mana pool.",
        "Counter spell and draw a card unless controller's mana pool is under 3.",
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
            {"U":(1,7)},
            least_mana={"colorless":1,"U":1}
        )

        self.room.env_stack_cards(self.player,self.card)
        simulate_info=self.room.simulate_play_in_stack(self.card)
        return simulate_info
