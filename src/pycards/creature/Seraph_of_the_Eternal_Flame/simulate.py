from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Seraph_of_the_Eternal_Flame.model import Seraph_of_the_Eternal_Flame

@bind_card(Seraph_of_the_Eternal_Flame)
class Seraph_of_the_Eternal_Flame_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Radiant Aura — Whenever [CARD_NAME] attacks, creatures you control gain indestructible until end of turn.",

        "Radiant Aura — Each time [CARD_NAME] attacks, creatures you control gain indestructible until end of turn.",

        "Radiant Aura — When [CARD_NAME] attacks, your creatures gain indestructible until end of turn.",

        "Radiant Aura — On attack, [CARD_NAME] grants indestructible to creatures you control until end of turn.",

        "Radiant Aura — Whenever [CARD_NAME] attacks, all creatures you control gain indestructible until end of turn.",

        "Radiant Aura — Whenever [CARD_NAME] attacks, creatures you control become indestructible until end of turn.",

        "Radiant Aura — Whenever [CARD_NAME] attacks, creatures you control can't be destroyed until end of turn.",

        "Radiant Aura — Whenever [CARD_NAME] attacks, your creatures are indestructible until end of turn.",

        "Radiant Aura — Whenever [CARD_NAME] attacks, creatures under your control gain indestructible until end of turn.",

    ]
