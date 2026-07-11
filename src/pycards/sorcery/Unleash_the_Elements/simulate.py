from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Unleash_the_Elements.model import Unleash_the_Elements

@bind_card(Unleash_the_Elements)
class Unleash_the_Elements_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 3 damage to each creature. If a creature dealt damage this way would die this turn, exile it instead.",

        "Deal 3 damage to every creature. If a creature dealt damage this way would die this turn, exile it instead.",

        "[CARD_NAME] inflicts 3 damage on each creature. Creatures that would die from this damage are exiled instead.",

        "Each creature takes 3 damage. If a creature dealt damage this way would die this turn, exile it rather than putting it into a graveyard.",

        "[CARD_NAME] deals three damage to all creatures. Any creature that would die from this damage is exiled instead.",

        "Deal 3 damage to each creature on the battlefield. If a creature dealt damage this way would die this turn, exile it instead of destroying it.",

        "[CARD_NAME] hits every creature for 3 damage. Creatures that would die from this damage are exiled this turn.",

        "All creatures take 3 damage. If a creature dealt damage this way would die this turn, exile it instead.",

        "[CARD_NAME] deals 3 damage to each creature. Instead of dying, creatures dealt damage this way are exiled if they would die this turn.",

        "Deal 3 damage to each creature. Exile any creature dealt damage this way that would die this turn."
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
            {"R": (1, 7), "G": (1, 7)},
            least_mana={"colorless": 1, "R": 1, "G": 1},
        )

        for creature in self.player.battlefield + self.player.opponent.battlefield:
            creature.actual_live = min(creature.actual_live, 3)

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
