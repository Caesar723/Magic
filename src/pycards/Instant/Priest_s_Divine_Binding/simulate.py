from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Priest_s_Divine_Binding.model import Priest_s_Divine_Binding

@bind_card(Priest_s_Divine_Binding)
class Priest_s_Divine_Binding_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target creature spell. You gain life equal to that creature's power.",
        "[CARD_NAME] counters target creature spell and you gain life equal to its power.",
        "Counter a creature spell. Gain life equal to the creature's power.",
        "With [CARD_NAME], counter creature spell and gain life equal to power.",
        "Counter target creature spell. You gain life equal to that creature's power.",
        "[CARD_NAME]: counter creature spell, gain life equal to power.",
        "Counter creature spells. Life gain equal to the creature's power.",
        "Counter a creature spell and gain life matching its power.",
        "[CARD_NAME] counters creature spells and heals you for the creature's power.",
        "Counter target creature spell; gain life equal to its power.",
    ]

    @simulate
    def simulate_card_stack(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"W":(1,7)},
            least_mana={"colorless":2,"W":1}
        )

        self.room.env_stack_cards(self.player,self.card)
        simulate_info=self.room.simulate_play_in_stack(self.card)
        return simulate_info
