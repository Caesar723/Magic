from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation
from pycards.sorcery.Pocket_Discovery.model import Pocket_Discovery


@bind_card(Pocket_Discovery)
class Pocket_Discovery_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Draw a card.",
        "Draw one card.",
        "Put the top card of your library into your hand."
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
        self.room.env_mana(self.player,{"U":(1,4)},least_mana={"colorless":0,"U":1})
        return self.room.simulate_play(self.card,preferred_subactions=(0,))
