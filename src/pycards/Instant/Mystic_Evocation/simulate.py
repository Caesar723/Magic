from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mystic_Evocation.model import Mystic_Evocation

@bind_card(Mystic_Evocation)
class Mystic_Evocation_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target noncreature spell. If that spell is countered this way, scry 2.",
        "[CARD_NAME] counters target noncreature spell; scry 2 if countered.",
        "Counter a noncreature spell. Scry 2 when countered this way.",
        "With [CARD_NAME], counter noncreature spell and scry 2 on successful counter.",
        "Counter target noncreature spell. If countered, scry 2.",
        "[CARD_NAME]: counter noncreature; scry 2 if countered.",
        "Counter noncreature spells only. Scry 2 if you counter it this way.",
        "Target noncreature spell is countered; scry 2 if countered by [CARD_NAME].",
        "Counter noncreature spell. On counter, look at top two and scry 2.",
        "[CARD_NAME] counters noncreature spells and lets you scry 2 when countered.",
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
