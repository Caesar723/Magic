from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Apocalypse_Riders.model import Apocalypse_Riders

@bind_card(Apocalypse_Riders)
class Apocalypse_Riders_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Summon four 2/2 Knight creature tokens, each with a different ability (Trample, Haste, Lifelink, Flying).",

        "[CARD_NAME] creates four 2/2 Knight creature tokens, each with a different keyword ability: Trample, Haste, Lifelink, and Flying.",

        "Create four 2/2 Knight tokens. One has trample, one has haste, one has lifelink, and one has flying.",

        "[CARD_NAME] summons four 2/2 Knight creature tokens with distinct abilities: Trample, Haste, Lifelink, and Flying.",

        "Put four 2/2 Knight creature tokens onto the battlefield, each granted a different ability among Trample, Haste, Lifelink, and Flying.",

        "[CARD_NAME] generates four 2/2 Knight creature tokens, each with one of Trample, Haste, Lifelink, or Flying.",

        "Summon four Knight creature tokens that are 2/2, each with a unique ability: Trample, Haste, Lifelink, or Flying.",

        "[CARD_NAME] places four 2/2 Knight tokens into play, each bearing a different ability from Trample, Haste, Lifelink, and Flying.",

        "Create four 2/2 Knight creature tokens. Each token has a different ability: Trample, Haste, Lifelink, or Flying.",

        "[CARD_NAME] brings four 2/2 Knight creature tokens onto the battlefield, each with a separate ability among Trample, Haste, Lifelink, and Flying."
    ]
