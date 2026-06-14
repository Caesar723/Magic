from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mystic_Tide.model import Mystic_Tide

@bind_card(Mystic_Tide)
class Mystic_Tide_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell unless its controller's mana pool is less than 3. If you control an Island, you may return random opponent's creature to its owner's hand.",
        "[CARD_NAME] counters unless controller has less than 3 mana; with an Island, bounce random opponent creature.",
        "Counter unless mana pool <3. If you control an Island, bounce random opponent creature.",
        "With [CARD_NAME], counter unless 3 mana available; Island lets you bounce random enemy creature.",
        "Counter target spell unless controller's mana is below 3. Island: bounce random opponent creature.",
        "[CARD_NAME]: counter unless mana <3; optional creature bounce if you control an Island.",
        "Unless controller has 3+ mana, counter target spell. Island control: bounce random opponent creature.",
        "Counter unless mana pool less than 3. You may bounce random opponent creature if you have an Island.",
        "[CARD_NAME] counters unless 3 mana; with Island, return random opponent creature to hand.",
        "Counter unless controller's mana pool is under 3. Island enables bouncing a random opponent creature.",
    ]
