from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Chaotic_Eruption.model import Chaotic_Eruption

@bind_card(Chaotic_Eruption)
class Chaotic_Eruption_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Destroy target land. For each land destroyed this way, its controller randomly discards a card.",

        "[CARD_NAME] destroys target land. For each land destroyed this way, its controller randomly discards a card.",

        "Destroy a target land. That land's controller randomly discards a card.",

        "[CARD_NAME] destroys target land and its controller randomly discards a card.",

        "Choose target land. Destroy it. Its controller randomly discards a card.",

        "[CARD_NAME] destroys a chosen target land. For each land destroyed this way, its controller randomly discards a card.",

        "Target land is destroyed. Its controller randomly discards a card.",

        "[CARD_NAME] causes target land to be destroyed. Its controller randomly discards a card.",

        "Destroy one target land. Its controller randomly discards a card.",

        "[CARD_NAME] destroys target land, and for each land destroyed this way, its controller randomly discards a card."
    ]
