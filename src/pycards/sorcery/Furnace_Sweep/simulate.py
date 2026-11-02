from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation
from pycards.sorcery.Furnace_Sweep.model import Furnace_Sweep


@bind_card(Furnace_Sweep)
class Furnace_Sweep_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 5 damage to each creature your opponent controls and 2 damage to your opponent.",
        "Deal 5 damage to every enemy creature and 2 damage to the opposing player.",
        "[CARD_NAME] hits all opposing creatures for five damage each and your opponent for two."
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
        damage=self.card.effect_params["damage"]
        for creature in self.player.opponent.battlefield:
            life=max(1,damage+random.choice((-1,0,1)))
            creature.live=creature.actual_live=life

        self.room.env_mana(self.player,{"R":(3,6)},least_mana={"colorless":3,"R":3})
        return self.room.simulate_play(self.card,preferred_subactions=(0,))
