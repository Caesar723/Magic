from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Cataclysmic_Surge.model import Cataclysmic_Surge

@bind_card(Cataclysmic_Surge)
class Cataclysmic_Surge_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 5 damage to each creature and each player.",

        "Deal 5 damage to every creature and every player.",

        "[CARD_NAME] inflicts 5 damage on each creature and each player.",

        "Each creature and each player takes 5 damage.",

        "[CARD_NAME] deals five damage to all creatures and all players.",

        "Deal 5 damage to each creature on the battlefield and each player.",

        "[CARD_NAME] hits every creature and every player for 5 damage.",

        "All creatures and all players take 5 damage.",

        "[CARD_NAME] deals 5 damage to each creature and each player in the game.",

        "Deal five damage to each creature and each player."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_creature(self.player)
        self.room.env_life_high(self.player)
        self.room.env_creature(self.player.opponent)
        self.room.env_life_high(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"R": (2, 7)},
            least_mana={"colorless": 2, "R": 2},
        )

        for creature in self.player.battlefield + self.player.opponent.battlefield:
            creature.actual_live = min(creature.actual_live, 5)

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
