from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Ethereal_Convergence.model import Ethereal_Convergence

@bind_card(Ethereal_Convergence)
class Ethereal_Convergence_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Return all creatures to their owners' hands. You may search your library for a creature card, reveal it, put it into your hand, then shuffle your library.",
        "[CARD_NAME] bounces all creatures, then lets you search your library for a creature card to hand.",
        "All creatures return to their owners' hands. You may tutor a creature into your hand.",
        "Return every creature to hand. Optionally search your library for a creature and put it in your hand.",
        "[CARD_NAME]: mass bounce all creatures; optional creature tutor to hand.",
        "Bounce all creatures. You may search for a creature card and put it into your hand.",
        "All creatures go back to hand. You may find a creature in your library and add it to hand.",
        "With [CARD_NAME], return all creatures to hand and optionally tutor a creature to hand.",
        "Return all creatures to owners' hands. Search library for a creature if you want.",
        "[CARD_NAME] returns all creatures to hand and may search your library for a creature card.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.room.env_initinal_library(self.player,{"creature_number":(1,10)})
        self.room.env_creature(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U":(2,7)},
            least_mana={"colorless":3,"U":2}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
