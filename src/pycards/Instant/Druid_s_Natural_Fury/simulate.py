from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Druid_s_Natural_Fury.model import Druid_s_Natural_Fury

@bind_card(Druid_s_Natural_Fury)
class Druid_s_Natural_Fury_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell. Then, create a green Beast creature token with power and toughness equal to that spell's mana cost.",
        "[CARD_NAME] counters target spell, then creates a green Beast token sized to that spell's mana cost.",
        "Counter a spell, then create a green Beast token with P/T equal to the countered spell's mana cost.",
        "With [CARD_NAME], counter target spell and spawn a green Beast token matching the spell's mana cost.",
        "Counter target spell. Create a green Beast creature token with power and toughness equal to its mana cost.",
        "[CARD_NAME]: counter a spell, then make a green Beast token with P/T equal to mana cost.",
        "Counter target spell, then put a green Beast token onto the battlefield equal to that spell's mana cost.",
        "Counter a spell and create a green Beast token with stats equal to the spell's mana cost.",
        "[CARD_NAME] counters target spell and summons a green Beast token sized to the spell's cost.",
        "Counter target spell. Then create a green Beast token with power and toughness equal to the spell's mana cost.",
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
            {"G":(1,7)},
            least_mana={"colorless":3,"G":1}
        )

        self.room.env_stack_cards(self.player,self.card)
        simulate_info=self.room.simulate_play_in_stack(self.card)
        return simulate_info
