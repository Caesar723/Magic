from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Arcane_Convergence.model import Arcane_Convergence

@bind_card(Arcane_Convergence)
class Arcane_Convergence_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] allows you to untap all lands you control and add X mana in any combination of colors to your mana pool, where X is the number of sorcery cards in your graveyard.",

        "Untap all lands you control. Add X mana in any combination of colors to your mana pool, where X is the number of sorcery cards in your graveyard.",

        "[CARD_NAME] untaps all your lands and adds X mana of any combination of colors, where X equals the number of sorcery cards in your graveyard.",

        "Untap all lands you control, then add X mana in any combination of colors, where X is the number of sorcery cards in your graveyard.",

        "[CARD_NAME] lets you untap all lands you control and add X mana in any colors, where X is the number of sorcery cards in your graveyard.",

        "Untap all lands you control. Add mana equal to the number of sorcery cards in your graveyard in any combination of colors.",

        "[CARD_NAME] untaps your lands and adds X mana in any combination of colors, where X is the count of sorcery cards in your graveyard.",

        "Untap all lands you control and add X mana in any combination of colors, where X is how many sorcery cards are in your graveyard.",

        "[CARD_NAME] allows you to untap all lands you control and add X mana of any colors, where X is the number of sorcery cards in your graveyard.",

        "Untap all lands you control. Add X mana in any combination of colors, where X is the number of sorcery cards in your graveyard."
    ]
