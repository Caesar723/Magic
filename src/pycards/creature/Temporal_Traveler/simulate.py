from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Temporal_Traveler.model import Temporal_Traveler

@bind_card(Temporal_Traveler)
class Temporal_Traveler_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Whenever [CARD_NAME] attacks, you may cast an instant or sorcery card from your graveyard without paying its mana cost.",

        "Each time [CARD_NAME] attacks, you may cast an instant or sorcery from your graveyard without paying its mana cost.",

        "When [CARD_NAME] attacks, you may cast an instant or sorcery card from your graveyard for free.",

        "Whenever [CARD_NAME] attacks, you may cast an instant or sorcery from your graveyard without paying mana.",

        "On attack, [CARD_NAME] lets you cast an instant or sorcery from your graveyard without paying its mana cost.",

        "Whenever [CARD_NAME] attacks, you may play an instant or sorcery from your graveyard without paying its mana cost.",

        "Whenever [CARD_NAME] attacks, you may cast an instant or sorcery spell from your graveyard without paying its mana cost.",

        "Whenever [CARD_NAME] attacks, you may cast an instant or sorcery card from your graveyard without paying mana.",

        "Whenever [CARD_NAME] attacks, you may cast an instant or sorcery from your graveyard without paying its mana cost.",

    ]
