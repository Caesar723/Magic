from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Falling_Stars.model import Falling_Stars

@bind_card(Falling_Stars)
class Falling_Stars_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Deal 7 damage to all creatures, then summon a 7/7 Star Beast creature token onto the battlefield.",

        "[CARD_NAME] deals 7 damage to each creature, then creates a 7/7 Star Beast creature token.",

        "All creatures take 7 damage. Then put a 7/7 Star Beast creature token onto the battlefield.",

        "[CARD_NAME] inflicts 7 damage on every creature, then summons a 7/7 Star Beast token.",

        "Deal seven damage to all creatures. Afterward, create a 7/7 Star Beast creature token.",

        "[CARD_NAME] deals 7 damage to all creatures on the battlefield, then places a 7/7 Star Beast creature token into play.",

        "Each creature takes 7 damage. Then you create a 7/7 Star Beast creature token.",

        "[CARD_NAME] hits all creatures for 7 damage, then puts a 7/7 Star Beast creature token onto the battlefield.",

        "Deal 7 damage to every creature, then generate a 7/7 Star Beast creature token.",

        "[CARD_NAME] deals 7 damage to all creatures and then summons a 7/7 Star Beast creature token onto the battlefield."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_creature(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"R": (2, 7)},
            least_mana={"colorless": 7, "R": 2},
        )

        for creature in self.player.battlefield + self.player.opponent.battlefield:
            creature.actual_live = min(creature.actual_live, 7)

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
