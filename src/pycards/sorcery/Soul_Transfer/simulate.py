from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Soul_Transfer.model import Soul_Transfer

@bind_card(Soul_Transfer)
class Soul_Transfer_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Choose one creature. That creature gains all die abilities of creature cards in your graveyard.",

        "[CARD_NAME] lets you choose a creature. That creature gains all die abilities of creature cards in your graveyard.",

        "Choose a creature. It gains every die ability from creature cards in your graveyard.",

        "[CARD_NAME] causes a chosen creature to gain all die abilities of creature cards in your graveyard.",

        "Select one creature. That creature acquires all die abilities of creature cards in your graveyard.",

        "[CARD_NAME] grants a chosen creature all die abilities found on creature cards in your graveyard.",

        "Choose one creature. That creature gains the die abilities of every creature card in your graveyard.",

        "[CARD_NAME] allows you to choose a creature, which gains all die abilities of creature cards in your graveyard.",

        "Pick one creature. It gains all die abilities of creature cards in your graveyard.",

        "[CARD_NAME] gives a chosen creature all die abilities of creature cards in your graveyard."
    ]
