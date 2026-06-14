from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Arcane_Reflection.model import Arcane_Reflection

@bind_card(Arcane_Reflection)
class Arcane_Reflection_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] allows return random instant or sorcery card from your graveyard to your hand.",
        "Return a random instant or sorcery card from your graveyard to your hand.",
        "[CARD_NAME] puts a random instant or sorcery from your graveyard into your hand.",
        "Retrieve a random instant or sorcery from your graveyard to your hand.",
        "With [CARD_NAME], return a random instant or sorcery from your graveyard to hand.",
        "Choose a random instant or sorcery in your graveyard and return it to your hand.",
        "[CARD_NAME] returns one random instant or sorcery card from your graveyard to your hand.",
        "Get back a random instant or sorcery from your graveyard to your hand.",
        "Return random instant or sorcery from graveyard to hand.",
        "[CARD_NAME] recovers a random instant or sorcery from your graveyard into your hand.",
    ]
