from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation
from pycards.sorcery.Deluge_of_Forgotten_Shores.model import Deluge_of_Forgotten_Shores


@bind_card(Deluge_of_Forgotten_Shores)
class Deluge_of_Forgotten_Shores_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Return all creatures your opponent controls to their owners' hands. Draw three cards.",
        "Return every opposing creature to its owner's hand, then draw 3 cards.",
        "All enemy creatures go back to their owners' hands. You draw three cards."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal({
            "graveyard":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(0,0)},
            "hand":{"creature_number":(0,1),"instant_number":(0,1),"sorcery_number":(0,1),"land_number":(0,1)},
            "library":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(6,8)},
        })
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)
        self.room.env_mana(self.player,{"U":(3,6)},least_mana={"colorless":6,"U":3})
        return self.room.simulate_play(self.card,preferred_subactions=(0,))
