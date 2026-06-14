from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Thalassian_Tidecaller.model import Thalassian_Tidecaller

@bind_card(Thalassian_Tidecaller)
class Thalassian_Tidecaller_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Whenever you cast a blue spell, you may draw a card.",

        "Each time you cast a blue spell, you may draw a card.",

        "When you cast a blue spell, you may draw a card.",

        "Whenever you cast a blue spell, you may draw one card.",

        "On casting a blue spell, you may draw a card.",

        "Whenever you play a blue spell, you may draw a card.",

        "Whenever you cast a blue spell, you may draw a card from your library.",

        "Each blue spell you cast lets you draw a card.",

        "Whenever you cast a blue spell, you may optionally draw a card.",

    ]
