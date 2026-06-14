from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Igni_the_Pyromancer.model import Igni_the_Pyromancer

@bind_card(Igni_the_Pyromancer)
class Igni_the_Pyromancer_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Whenever [CARD_NAME] deals damage to a player, you randomly cast an instant or sorcery spell from your graveyard without paying its mana cost.",

        "Each time [CARD_NAME] deals damage to a player, you randomly cast an instant or sorcery from your graveyard without paying its mana cost.",

        "When [CARD_NAME] deals damage to a player, you randomly cast an instant or sorcery spell from your graveyard for free.",

        "Whenever [CARD_NAME] damages a player, you randomly cast an instant or sorcery from your graveyard without paying mana.",

        "On dealing damage to a player, [CARD_NAME] lets you randomly cast an instant or sorcery from your graveyard without paying its mana cost.",

        "Whenever [CARD_NAME] deals damage to a player, randomly cast an instant or sorcery spell from your graveyard without paying its mana cost.",

        "Whenever [CARD_NAME] deals damage to a player, you cast a random instant or sorcery from your graveyard without paying its mana cost.",

        "Whenever [CARD_NAME] deals damage to a player, you randomly play an instant or sorcery from your graveyard without paying its mana cost.",

        "Whenever [CARD_NAME] deals damage to a player, you randomly cast an instant or sorcery card from your graveyard without paying its mana cost.",

    ]
