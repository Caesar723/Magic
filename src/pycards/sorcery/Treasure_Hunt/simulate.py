from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Treasure_Hunt.model import Treasure_Hunt

@bind_card(Treasure_Hunt)
class Treasure_Hunt_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Return a card from your graveyard to your hand.",

        "[CARD_NAME] lets you return a card from your graveyard to your hand.",

        "Return one card from your graveyard to your hand.",

        "[CARD_NAME] returns a card from your graveyard to your hand.",

        "Choose a card in your graveyard. Return it to your hand.",

        "[CARD_NAME] allows you to return a card from your graveyard to your hand.",

        "Put a card from your graveyard into your hand.",

        "[CARD_NAME] brings a card from your graveyard back to your hand.",

        "Return a target card from your graveyard to your hand.",

        "[CARD_NAME] returns one card from your graveyard to your hand."
    ]
