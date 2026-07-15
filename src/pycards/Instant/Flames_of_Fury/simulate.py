from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Flames_of_Fury.model import Flames_of_Fury

@bind_card(Flames_of_Fury)
class Flames_of_Fury_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 3 damage to any target. If a creature dealt damage this way would die this turn, exile it instead.",
        "Deal 3 damage to any target. Exile creatures that would die from this damage this turn.",
        "[CARD_NAME] hits any target for 3; creatures that would die from it are exiled instead.",
        "Choose any target. Deal 3 damage. Creatures that would die this turn are exiled.",
        "Deal 3 damage to any target. If a creature would die from [CARD_NAME] this turn, exile it.",
        "[CARD_NAME]: 3 damage to any target; exile instead of die this turn.",
        "Any target takes 3 damage. Creatures that would die from this are exiled this turn.",
        "Inflict 3 damage on any target. Exile creatures that would die from this damage.",
        "[CARD_NAME] deals 3 and exiles creatures that would die from the damage this turn.",
        "Three damage to any target; creatures killed this way are exiled instead.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.room.env_creature(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)
        for creature in self.player.battlefield+self.player.opponent.battlefield:
            creature.live=min(creature.live,3)
            creature.actual_live=creature.live

        self.room.env_mana(
            self.player,
            {"R":(1,7)},
            least_mana={"colorless":1,"R":1}
        )

        simulate_info=self.room.simulate_play(self.card,preferred_subactions=range(1,21))
        return simulate_info
