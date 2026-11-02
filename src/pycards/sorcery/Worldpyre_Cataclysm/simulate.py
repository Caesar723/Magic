from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation
from pycards.sorcery.Worldpyre_Cataclysm.model import Worldpyre_Cataclysm


@bind_card(Worldpyre_Cataclysm)
class Worldpyre_Cataclysm_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 7 damage to each creature your opponent controls and 5 damage to your opponent.",
        "Deal 7 damage to all opposing creatures and 5 damage to the opposing player.",
        "[CARD_NAME] burns each enemy creature for seven damage and your opponent for five."
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
        self.room.env_mana(self.player,{"R":(3,6)},least_mana={"colorless":6,"R":3})
        return self.room.simulate_play(self.card,preferred_subactions=(0,))
