from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Essence_Channeler.model import Essence_Channeler

@bind_card(Essence_Channeler)
class Essence_Channeler_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Whenever you cast a creature spell, you may add G to your mana pool.",

        "Each time you cast a creature spell, you may add G to your mana pool.",

        "When you cast a creature spell, you may add G to your mana pool.",

        "Whenever you cast a creature, you may add G to your mana pool.",

        "On casting a creature spell, you may add G to your mana pool.",

        "Whenever you cast a creature spell, you may add one green mana to your mana pool.",

        "Whenever you cast a creature spell, you may add G mana to your mana pool.",

        "Whenever you cast a creature spell, you may add green mana to your mana pool.",

        "Each creature spell you cast lets you add G to your mana pool.",

    ]
