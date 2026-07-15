from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Blaze_of_Fury.model import Blaze_of_Fury

@bind_card(Blaze_of_Fury)
class Blaze_of_Fury_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 3 damage to any target. If a creature is dealt damage this way, tap it.",
        "Deal 3 damage to any target. If a creature is dealt damage this way, tap it.",
        "[CARD_NAME] hits any target for 3. Tap any creature damaged this way.",
        "Choose any target. Deal 3 damage. Tap creatures damaged this way.",
        "Deal 3 damage to any target; tap creatures that take damage from [CARD_NAME].",
        "[CARD_NAME] deals 3 to any target and taps creatures damaged by it.",
        "Any target takes 3 damage. Tap creatures dealt damage this way.",
        "Inflict 3 damage on any target. Tap creatures damaged by [CARD_NAME].",
        "Deal 3 damage to any target. Creatures damaged this way become tapped.",
        "[CARD_NAME]: 3 damage to any target; tap creatures hit this way.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.room.env_creature(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)
        for creature in self.player.battlefield+self.player.opponent.battlefield:
            creature.live=max(creature.live,4)
            creature.actual_live=creature.live

        self.room.env_mana(
            self.player,
            {"R":(2,7)},
            least_mana={"colorless":1,"R":2}
        )

        simulate_info=self.room.simulate_play(self.card,preferred_subactions=range(1,21))
        return simulate_info
