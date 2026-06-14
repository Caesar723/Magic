from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Verdant_Titan.model import Verdant_Titan

@bind_card(Verdant_Titan)
class Verdant_Titan_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Trample, Vigilance. When [CARD_NAME] enters the battlefield or attacks, you may search your library for a land card and put it onto the battlefield tapped. If you do, shuffle your library.",

        "Vigilance, Trample. When [CARD_NAME] enters the battlefield or attacks, you may search your library for a land, put it onto the battlefield tapped, then shuffle if you do.",

        "Trample, Vigilance. On entering or attacking, [CARD_NAME] lets you search for a land, put it onto the battlefield tapped, and shuffle if you do.",

        "Vigilance, Trample. When [CARD_NAME] enters or attacks, you may find a land, put it onto the battlefield tapped, then shuffle your library if you do.",

        "Trample, Vigilance. When [CARD_NAME] enters the battlefield or attacks, you may search for a land card, put it onto the battlefield tapped, shuffle if you do.",

        "Vigilance, Trample. When [CARD_NAME] enters the battlefield or attacks, you may search your library for a land card, place it onto the battlefield tapped, then shuffle if you do.",

        "Trample, Vigilance. When [CARD_NAME] enters or attacks, you may search your library for a land and put it onto the battlefield tapped. Shuffle if you do.",

        "Vigilance, Trample. When [CARD_NAME] enters the battlefield or attacks, you may search your library for a land, put it on the battlefield tapped, shuffle if you do.",

        "Trample, Vigilance. When [CARD_NAME] enters the battlefield or attacks, you may search your library for a land card, put it onto the battlefield tapped. Shuffle your library if you do.",

    ]
