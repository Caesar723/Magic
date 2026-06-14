from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Vengeful_Wrath.model import Vengeful_Wrath

@bind_card(Vengeful_Wrath)
class Vengeful_Wrath_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Destroy target creature. Deal damage equal to its power to a random creature your opponent controls.",
        "[CARD_NAME] destroys target creature and deals its power as damage to a random opponent creature.",
        "Destroy a creature. Damage a random opponent creature equal to destroyed creature's power.",
        "Choose target creature. Destroy it. Random opponent creature takes damage equal to its power.",
        "[CARD_NAME]: destroy creature; random opponent creature takes damage equal to power.",
        "Slay target creature. Splash its power as damage to random opponent creature.",
        "Destroy target creature. Its power is dealt to a random creature your opponent controls.",
        "With [CARD_NAME], destroy a creature and hit random opponent creature for its power.",
        "Target creature destroyed. Random opponent creature takes damage equal to its power.",
        "[CARD_NAME] destroys a creature and vengefully damages a random opponent creature.",
    ]
