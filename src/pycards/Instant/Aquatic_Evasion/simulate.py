from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Aquatic_Evasion.model import Aquatic_Evasion

@bind_card(Aquatic_Evasion)
class Aquatic_Evasion_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target creature you control gains hexproof until end of turn. Draw a card.",
        "[CARD_NAME] gives target creature you control hexproof until end of turn and lets you draw a card.",
        "Choose a creature you control. It gains hexproof until end of turn. Draw a card.",
        "Until end of turn, a creature you control can't be the target of spells or abilities. Draw a card.",
        "[CARD_NAME] grants hexproof to a creature you control until end of turn, then you draw a card.",
        "Target your creature with [CARD_NAME]. It gains hexproof until end of turn. Draw a card.",
        "Give target creature you control hexproof until end of turn, then draw a card.",
        "A creature you control gains protection from targeting until end of turn. Draw a card.",
        "[CARD_NAME]: hexproof on a creature you control until end of turn, plus draw a card.",
        "Target creature you control has hexproof this turn. Draw a card.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.room.env_creature(self.player)
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
