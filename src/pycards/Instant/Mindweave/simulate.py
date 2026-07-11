from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mindweave.model import Mindweave

@bind_card(Mindweave)
class Mindweave_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell unless its controller's mana pool is less than 2. If that spell is countered this way, you may draw 1 cards.",
        "[CARD_NAME] counters target spell unless controller has less than 2 mana; draw if countered.",
        "Counter unless controller's mana pool is under 2. Draw a card if countered this way.",
        "With [CARD_NAME], counter target spell unless controller has fewer than 2 mana; optional draw on counter.",
        "Counter target spell unless mana pool <2. You may draw if countered.",
        "[CARD_NAME]: counter unless mana pool less than 2; draw on counter.",
        "Unless controller has at least 2 mana, counter target spell. Draw if countered.",
        "Counter target spell unless controller's mana is below 2. Draw a card if you counter it.",
        "[CARD_NAME] counters unless 2 mana available; draw when countered this way.",
        "Counter unless controller's mana pool is less than 2. May draw if countered.",
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
            least_mana={"U":2}
        )

        self.room.env_stack_cards(self.player,self.card)
        simulate_info=self.room.simulate_play_in_stack(self.card)
        return simulate_info
