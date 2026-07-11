from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Chaos_Unleashed.model import Chaos_Unleashed

@bind_card(Chaos_Unleashed)
class Chaos_Unleashed_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 3 damage to each creature and each player.",

        "Deal 3 damage to every creature and every player.",

        "[CARD_NAME] inflicts 3 damage on each creature and each player.",

        "Each creature and each player takes 3 damage.",

        "[CARD_NAME] deals three damage to all creatures and all players.",

        "Deal 3 damage to each creature on the battlefield and each player.",

        "[CARD_NAME] hits every creature and every player for 3 damage.",

        "All creatures and all players take 3 damage.",

        "[CARD_NAME] deals 3 damage to each creature and each player in the game.",

        "Deal three damage to each creature and each player."
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
            {"B": (1, 7), "R": (1, 7)},
            least_mana={"colorless": 1, "B": 1, "R": 1},
        )

        for creature in self.player.battlefield + self.player.opponent.battlefield:
            creature.actual_live = min(creature.actual_live, 3)

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
