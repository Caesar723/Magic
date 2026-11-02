from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation
from pycards.sorcery.Wildheart_Ascendancy.model import Wildheart_Ascendancy


@bind_card(Wildheart_Ascendancy)
class Wildheart_Ascendancy_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Creatures you control get +3/+3 and gain trample until end of turn.",
        "Until the turn ends, all your creatures gain +3/+3 and trample.",
        "Give each creature you control three additional power, three additional toughness, and trample for this turn."
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
        self.room.env_mana(self.player,{"G":(2,5)},least_mana={"colorless":3,"G":2})
        return self.room.simulate_play(self.card,preferred_subactions=(0,))
