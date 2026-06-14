from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Ephemeral_Eruption.model import Ephemeral_Eruption

@bind_card(Ephemeral_Eruption)
class Ephemeral_Eruption_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 4 damage to each creature. At the beginning of the next end step, return all creatures killed by this way to the battlefield under their owner's control.",

        "Deal 4 damage to every creature. At the beginning of the next end step, return all creatures killed this way to the battlefield under their owner's control.",

        "[CARD_NAME] inflicts 4 damage on each creature. At the next end step, return all creatures killed this way to the battlefield.",

        "Each creature takes 4 damage. At the beginning of the next end step, return all creatures killed this way to the battlefield under their owner's control.",

        "[CARD_NAME] deals 4 damage to all creatures. At the beginning of the next end step, creatures killed this way return to the battlefield under their owner's control.",

        "Deal 4 damage to each creature. At the beginning of the next end step, return each creature killed this way to the battlefield under its owner's control.",

        "[CARD_NAME] hits every creature for 4 damage. At the next end step, return all creatures killed this way to the battlefield.",

        "All creatures take 4 damage. At the beginning of the next end step, return all creatures killed this way to the battlefield under their owner's control.",

        "[CARD_NAME] deals 4 damage to each creature. At the beginning of the next end step, return creatures killed this way to the battlefield under their owner's control.",

        "Deal 4 damage to each creature. At the beginning of the next end step, return all creatures killed by [CARD_NAME] to the battlefield under their owner's control."
    ]
