from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation
from pycards.sorcery.Twin_Current_Recall.model import Twin_Current_Recall


@bind_card(Twin_Current_Recall)
class Twin_Current_Recall_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Return all creatures your opponent controls with power 3 or less to their owners' hands. Draw two cards.",
        "Return every opposing creature with power at most 3 to its owner's hand, then draw 2 cards.",
        "Enemy creatures with power three or lower return to their owners' hands. You draw two cards."
    ]

    @simulate
    def simulate_low_power(self):
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
        threshold=self.card.effect_params["power_threshold"]
        self.player.opponent.battlefield=[]
        self.stage_card(Testing_Spawn_Creature(self.player.opponent,max(0,threshold-1),5),self.player.opponent)
        self.stage_card(Testing_Spawn_Creature(self.player.opponent,threshold,5),self.player.opponent)
        self.room.env_mana(self.player,{"U":(3,6)},least_mana={"colorless":3,"U":3})
        return self.room.simulate_play(self.card,preferred_subactions=(0,))

    @simulate
    def simulate_high_power(self):
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
        threshold=self.card.effect_params["power_threshold"]
        self.player.opponent.battlefield=[]
        self.stage_card(Testing_Spawn_Creature(self.player.opponent,threshold+1,5),self.player.opponent)
        self.stage_card(Testing_Spawn_Creature(self.player.opponent,threshold+3,5),self.player.opponent)
        self.room.env_mana(self.player,{"U":(3,6)},least_mana={"colorless":3,"U":3})
        return self.room.simulate_play(self.card,preferred_subactions=(0,))

    @simulate
    def simulate_mixed_power(self):
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
        threshold=self.card.effect_params["power_threshold"]
        self.player.opponent.battlefield=[]
        self.stage_card(Testing_Spawn_Creature(self.player.opponent,threshold,5),self.player.opponent)
        self.stage_card(Testing_Spawn_Creature(self.player.opponent,threshold+1,5),self.player.opponent)
        self.room.env_mana(self.player,{"U":(3,6)},least_mana={"colorless":3,"U":3})
        return self.room.simulate_play(self.card,preferred_subactions=(0,))
