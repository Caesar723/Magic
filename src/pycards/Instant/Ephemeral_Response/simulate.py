from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Ephemeral_Response.model import Ephemeral_Response

@bind_card(Ephemeral_Response)
class Ephemeral_Response_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell unless its controller pays 2. If it is countered this way, scry 1.",
        "[CARD_NAME] counters target spell unless its controller pays 2. If countered, scry 1.",
        "Counter target spell unless the controller pays 2 mana. Scry 1 if countered this way.",
        "Unless its controller pays 2, counter target spell. Scry 1 when countered this way.",
        "[CARD_NAME]: counter unless pay 2; scry 1 if countered.",
        "Target spell is countered unless its controller pays 2. Scry 1 if you counter it this way.",
        "Counter a spell unless controller pays 2. If countered, look at the top of your library and scry 1.",
        "With [CARD_NAME], counter target spell unless pay 2; scry 1 on successful counter.",
        "Counter target spell unless 2 is paid. If countered this way, scry 1.",
        "[CARD_NAME] counters unless its controller pays 2; scry 1 when countered this way.",
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
            least_mana={"colorless":2,"U":1}
        )

        self.room.env_stack_cards(self.player)
        simulate_info=self.room.simulate_play_in_stack(self.card)
        return simulate_info
