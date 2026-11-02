from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation
from pycards.Instant.Cinder_Needle.model import Cinder_Needle


@bind_card(Cinder_Needle)
class Cinder_Needle_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 2 damage to target creature an opponent controls.",
        "Deal 2 damage to a target opposing creature.",
        "[CARD_NAME] deals two damage to target creature controlled by an opponent."
    ]

    @simulate
    def simulate_lethal(self):
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
        self.stage_card(Testing_Spawn_Creature(self.player.opponent,2,1),self.player.opponent)
        self.room.env_mana(self.player,{"R":(1,4)},least_mana={"colorless":0,"R":1})
        return self.room.simulate_play(self.card,preferred_subactions=(1,))

    @simulate
    def simulate_nonlethal(self):
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
        self.stage_card(Testing_Spawn_Creature(self.player.opponent,2,3),self.player.opponent)
        self.room.env_mana(self.player,{"R":(1,4)},least_mana={"colorless":0,"R":1})
        return self.room.simulate_play(self.card,preferred_subactions=(1,))
