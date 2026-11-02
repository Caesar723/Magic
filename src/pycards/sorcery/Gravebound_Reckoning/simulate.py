from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation
from pycards.sorcery.Gravebound_Reckoning.model import Gravebound_Reckoning


@bind_card(Gravebound_Reckoning)
class Gravebound_Reckoning_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Destroy target creature an opponent controls. You gain 3 life.",
        "Destroy a target opposing creature, then gain 3 life.",
        "Eliminate target creature controlled by an opponent. Restore three life to yourself."
    ]

    @simulate
    def simulate_target_creature(self):
        self.basic_initinal({
            "graveyard":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(0,0)},
            "hand":{"creature_number":(0,1),"instant_number":(0,1),"sorcery_number":(0,1),"land_number":(0,1)},
            "library":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(6,8)},
        })
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)
        from game.testing_room import Testing_Spawn_Creature
        self.player.opponent.battlefield=[]
        self.stage_card(Testing_Spawn_Creature(self.player.opponent,3,5),self.player.opponent)
        heal=self.card.effect_params["heal"]
        missing=random.choice((0,1,heal,heal+1,self.player.ini_life-1))
        self.player.life=max(1,self.player.ini_life-missing)

        self.room.env_mana(self.player,{"B":(2,5)},least_mana={"colorless":3,"B":2})
        return self.room.simulate_play(self.card,preferred_subactions=(1,))
