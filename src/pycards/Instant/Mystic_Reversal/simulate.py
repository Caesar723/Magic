from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mystic_Reversal.model import Mystic_Reversal

@bind_card(Mystic_Reversal)
class Mystic_Reversal_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell. If that spell is countered this way, its controller may cast it without paying its mana cost during their next turn.",
        "[CARD_NAME] counters target spell; controller may recast it free next turn if countered.",
        "Counter a spell. If countered this way, controller may cast it free on their next turn.",
        "With [CARD_NAME], counter target spell; owner gets a free recast next turn if countered.",
        "Counter target spell. On counter, controller may cast it without paying next turn.",
        "[CARD_NAME]: counter spell; free recast for controller next turn if countered.",
        "Counter target spell. If countered, its controller may replay it free next turn.",
        "Counter a spell. Countered spells may be cast free by controller next turn.",
        "[CARD_NAME] counters and grants a free recast next turn to the spell's controller.",
        "Counter target spell. Controller may cast it without paying mana during their next turn if countered.",
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
