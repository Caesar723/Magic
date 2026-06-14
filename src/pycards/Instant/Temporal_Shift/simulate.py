from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Temporal_Shift.model import Temporal_Shift

@bind_card(Temporal_Shift)
class Temporal_Shift_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Randomly freeze up to two enemy creatures and halve their health.Add a time counter. When it reaches 10, take an extra turn.",
        "[CARD_NAME] randomly freezes up to two enemy creatures, halves their health, and adds a time counter toward an extra turn at 10.",
        "Freeze up to two random enemy creatures and halve health. Time counter: extra turn at 10.",
        "Randomly freeze two enemy creatures, halve health, add time counter for extra turn at 10.",
        "[CARD_NAME]: random freeze up to two enemies, halve health, time counter for extra turn.",
        "Freeze random enemy creatures (up to two), halve health. Time counter grants extra turn at 10.",
        "Up to two random enemy creatures frozen with halved health. Time counter toward extra turn.",
        "With [CARD_NAME], freeze enemies, halve health, accumulate time counter for extra turn at 10.",
        "Random freeze up to two opponents' creatures, halve health, time counter for bonus turn.",
        "[CARD_NAME] freezes enemies, halves health, and builds time counter toward extra turn.",
    ]
