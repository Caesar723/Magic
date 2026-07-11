from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Divine_Intervention.model import Divine_Intervention

@bind_card(Divine_Intervention)
class Divine_Intervention_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Choose up to two target creatures. Prevent all damage that would be dealt to those creatures this turn. Gain life equal to the total damage prevented this way.",
        "[CARD_NAME] protects up to two creatures from all damage this turn; gain life equal to damage prevented.",
        "Up to two target creatures can't be dealt damage this turn. Gain life equal to total damage prevented.",
        "Prevent all damage to up to two target creatures this turn. Gain life equal to damage prevented.",
        "[CARD_NAME]: shield up to two creatures from damage this turn; gain life equal to prevented damage.",
        "Choose up to two creatures. Prevent damage to them this turn. Gain life equal to damage prevented.",
        "Protect up to two target creatures from damage this turn. You gain life equal to damage prevented.",
        "With [CARD_NAME], prevent damage to up to two creatures and gain life equal to damage prevented.",
        "Up to two creatures are protected from damage this turn. Gain life equal to total prevented damage.",
        "[CARD_NAME] prevents damage to up to two creatures and grants life equal to damage prevented.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.room.env_creature(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"W":(1,7)},
            least_mana={"colorless":1,"W":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
