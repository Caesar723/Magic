from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Swift_Ward.model import Swift_Ward

@bind_card(Swift_Ward)
class Swift_Ward_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target creature gets +1/+1 until end of turn and gains hexproof until end of turn.",
        "[CARD_NAME] gives +1/+1 and hexproof until end of turn to target creature.",
        "Choose a creature. +1/+1 and hexproof this turn.",
        "Buff target creature +1/+1 and hexproof until end of turn.",
        "[CARD_NAME]: +1/+1 and hexproof until end of turn.",
        "Target creature gets +1/+1 and can't be targeted until end of turn.",
        "+1/+1 and hexproof on target creature this turn.",
        "With [CARD_NAME], grant +1/+1 and hexproof until end of turn.",
        "Give target creature +1/+1 and hexproof this turn.",
        "[CARD_NAME] wards a creature with +1/+1 and hexproof until end of turn.",
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
            {"W":(1,7)},
            least_mana={"colorless":1,"W":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
