from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Overgrowth_Surge.model import Overgrowth_Surge

@bind_card(Overgrowth_Surge)
class Overgrowth_Surge_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target creature gets +3/+3 until end of turn. If that creature is a Treefolk, it also gains trample until end of turn.",
        "[CARD_NAME] gives +3/+3 until end of turn; Treefolk also gain trample.",
        "Choose a creature. +3/+3 this turn. Treefolk also get trample.",
        "Buff target creature +3/+3. Treefolk gain trample too.",
        "[CARD_NAME]: +3/+3; Treefolk also trample until end of turn.",
        "Target creature gets +3/+3. If Treefolk, it gains trample this turn.",
        "+3/+3 until end of turn. Treefolk also trample.",
        "With [CARD_NAME], +3/+3 buff; Treefolk get trample as well.",
        "Give +3/+3 until end of turn. Treefolk also gain trample.",
        "[CARD_NAME] buffs a creature +3/+3 and grants Treefolk trample.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.room.env_creature(self.player)
        # Make the sampled target a Treefolk so the conditional trample branch fires.
        for creature in self.player.battlefield:
            creature.type_creature="Treefolk"
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"G":(1,7)},
            least_mana={"colorless":1,"G":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
