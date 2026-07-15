from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Verdant_Surge.model import Verdant_Surge

@bind_card(Verdant_Surge)
class Verdant_Surge_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target creature you control gets +2/+4 until end of turn. If that creature is a Druid, it also gains reach until end of turn.",
        "[CARD_NAME] gives your creature +2/+4; Druids also gain reach until end of turn.",
        "Choose your creature. +2/+4 this turn. Druids also get reach.",
        "Buff your creature +2/+4. Druid creatures gain reach too.",
        "[CARD_NAME]: +2/+4 on your creature; Druids gain reach.",
        "Target creature you control gets +2/+4. Druids also reach until end of turn.",
        "+2/+4 until end of turn on your creature. Druids gain reach.",
        "With [CARD_NAME], +2/+4 buff; Druids get reach as well.",
        "Your creature gets +2/+4. If Druid, also reach this turn.",
        "[CARD_NAME] surges your creature +2/+4 and grants Druids reach.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.room.env_creature(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)
        for creature in self.player.battlefield+self.player.opponent.battlefield:
            creature.type_creature="Druid"

        self.room.env_mana(
            self.player,
            {"G":(2,7)},
            least_mana={"colorless":1,"G":2}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
