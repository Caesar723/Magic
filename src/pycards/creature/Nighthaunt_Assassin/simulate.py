from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Nighthaunt_Assassin.model import Nighthaunt_Assassin

@bind_card(Nighthaunt_Assassin)
class Nighthaunt_Assassin_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you may destroy a random creature an opponent controls with converted mana cost 2 or less.",

        "When [CARD_NAME] enters play, you may destroy a random opposing creature with mana value 2 or less.",

        "As [CARD_NAME] enters the battlefield, you may destroy a random creature an opponent controls with CMC 2 or less.",

        "Upon entering the battlefield, [CARD_NAME] lets you destroy a random opposing creature with converted mana cost 2 or less.",

        "When [CARD_NAME] arrives, you may destroy a random creature an opponent controls with mana value 2 or less.",

        "When [CARD_NAME] enters the battlefield, you may destroy a random opponent's creature with converted mana cost 2 or less.",

        "When [CARD_NAME] enters the battlefield, you may destroy a random creature an opponent controls costing 2 or less.",

        "When [CARD_NAME] enters the battlefield, you may destroy a random opposing creature with CMC 2 or less.",

        "When [CARD_NAME] enters the battlefield, you may destroy a random creature an opponent controls with mana cost 2 or less.",

    ]
