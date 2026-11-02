from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation
from pycards.sorcery.Sanctuary_Judgment.model import Sanctuary_Judgment


@bind_card(Sanctuary_Judgment)
class Sanctuary_Judgment_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Destroy all creatures, then create two 2/2 white Knight creature tokens.",
        "Destroy every creature on the battlefield. Afterward, summon two white 2/2 Knight tokens.",
        "All creatures are destroyed, then you create two 2/2 white Knights."
    ]

    @simulate
    def simulate_empty_battlefield(self):
        self.basic_initinal({
            "graveyard":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(0,0)},
            "hand":{"creature_number":(0,1),"instant_number":(0,1),"sorcery_number":(0,1),"land_number":(0,1)},
            "library":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(6,8)},
        })
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)
        self.room.env_no_creature(self.player)
        self.room.env_mana(self.player,{"W":(3,6)},least_mana={"colorless":5,"W":3})
        return self.room.simulate_play(self.card,preferred_subactions=(0,))

    @simulate
    def simulate_occupied_battlefield(self):
        self.basic_initinal({
            "graveyard":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(0,0)},
            "hand":{"creature_number":(0,1),"instant_number":(0,1),"sorcery_number":(0,1),"land_number":(0,1)},
            "library":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(6,8)},
        })
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)
        self.room.env_one_creature(self.player)
        self.room.env_mana(self.player,{"W":(3,6)},least_mana={"colorless":5,"W":3})
        return self.room.simulate_play(self.card,preferred_subactions=(0,))
