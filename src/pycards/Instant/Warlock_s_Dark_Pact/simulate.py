from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Warlock_s_Dark_Pact.model import Warlock_s_Dark_Pact

@bind_card(Warlock_s_Dark_Pact)
class Warlock_s_Dark_Pact_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell. Its controller loses life equal to its mana cost.",
        "[CARD_NAME] counters target spell; its controller loses life equal to mana cost.",
        "Counter a spell. Controller loses life equal to its mana cost.",
        "With [CARD_NAME], counter target spell and drain life from controller equal to cost.",
        "Counter target spell. Spell controller loses life equal to mana cost.",
        "[CARD_NAME]: counter spell; life loss to controller equal to mana cost.",
        "Counter a spell. Its controller loses life matching the spell's mana cost.",
        "Counter target spell. Controller takes life loss equal to mana cost.",
        "[CARD_NAME] counters and makes controller lose life equal to mana cost.",
        "Counter spell; controller loses life equal to its mana cost.",
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
            {"B":(1,7)},
            least_mana={"colorless":2,"B":1}
        )

        self.room.env_stack_cards(self.player,self.card)
        simulate_info=self.room.simulate_play_in_stack(self.card)
        return simulate_info
