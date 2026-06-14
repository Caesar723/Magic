from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Divine_Intervention.model import Divine_Intervention

@bind_card(Divine_Intervention)
class Divine_Intervention_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Exile all nonland permanents. For each permanent exiled this way, its controller may search their library for a basic land card and put it onto the battlefield tapped.",

        "[CARD_NAME] exiles all nonland permanents. For each permanent exiled this way, its controller may search their library for a basic land and put it onto the battlefield tapped.",

        "Exile every nonland permanent. Each controller of a permanent exiled this way may search their library for a basic land and put it onto the battlefield tapped.",

        "[CARD_NAME] removes all nonland permanents from the game. For each one exiled, its controller may find a basic land and put it onto the battlefield tapped.",

        "Exile all nonland permanents. For each permanent exiled this way, that permanent's controller may search their library for a basic land card and put it onto the battlefield tapped.",

        "[CARD_NAME] exiles all nonland permanents. Each controller of an exiled permanent may search their library for a basic land and put it onto the battlefield tapped.",

        "All nonland permanents are exiled. For each permanent exiled this way, its controller may search their library for a basic land and put it onto the battlefield tapped.",

        "[CARD_NAME] exiles every nonland permanent. For each permanent exiled, its controller may search their library for a basic land card and put it onto the battlefield tapped.",

        "Exile all nonland permanents from the battlefield. For each permanent exiled this way, its controller may search their library for a basic land and put it onto the battlefield tapped.",

        "[CARD_NAME] exiles all nonland permanents. For each permanent exiled this way, its controller may search their library for a basic land and put it onto the battlefield tapped."
    ]
