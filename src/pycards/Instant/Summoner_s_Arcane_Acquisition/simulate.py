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
