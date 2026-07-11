from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Summoner_s_Arcane_Acquisition.model import Summoner_s_Arcane_Acquisition

@bind_card(Summoner_s_Arcane_Acquisition)
class Summoner_s_Arcane_Acquisition_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell. If the spell is countered this way, create an Elemental creature token with power and toughness equal to that spell's mana cost.",
        "[CARD_NAME] counters target spell and creates an Elemental token sized to the spell's mana cost.",
        "Counter a spell. On counter, create Elemental token with P/T equal to mana cost.",
        "With [CARD_NAME], counter target spell and summon Elemental token matching mana cost.",
        "Counter target spell. Elemental token with P/T equal to mana cost if countered.",
        "[CARD_NAME]: counter spell; Elemental token equal to mana cost.",
        "Counter a spell and create Elemental token with stats equal to its mana cost.",
        "Counter target spell. Spawn Elemental with P/T equal to countered spell's cost.",
        "[CARD_NAME] counters and creates an Elemental token sized to the spell's mana cost.",
        "Counter spell; Elemental token with power and toughness equal to mana cost.",
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
            least_mana={"colorless":2,"G":1}
        )

        self.room.env_stack_cards(self.player,self.card)
        simulate_info=self.room.simulate_play_in_stack(self.card)
        return simulate_info
