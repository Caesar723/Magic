from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation
from pycards.Instant.Giantbreaker_Spark.model import Giantbreaker_Spark


@bind_card(Giantbreaker_Spark)
class Giantbreaker_Spark_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 6 damage to target creature an opponent controls if its power is 4 or greater. Otherwise, it deals 3 damage to that creature.",
        "Deal 6 damage to a target opposing creature with power at least 4; if its power is lower, deal 3 damage instead.",
        "Target an enemy creature. It takes six damage if its power is four or more, and three damage otherwise."
    ]

    @simulate
    def simulate_power_3(self):
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
        threshold=self.card.effect_params["power_threshold"]
        life=max(self.card.effect_params["damage_low"],self.card.effect_params["damage_high"])+1
        self.stage_card(Testing_Spawn_Creature(self.player.opponent,max(0,threshold-1),life),self.player.opponent)
        self.room.env_mana(self.player,{"R":(2,5)},least_mana={"colorless":1,"R":2})
        return self.room.simulate_play(self.card,preferred_subactions=(1,))

    @simulate
    def simulate_power_4(self):
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
        threshold=self.card.effect_params["power_threshold"]
        life=max(self.card.effect_params["damage_low"],self.card.effect_params["damage_high"])+1
        self.stage_card(Testing_Spawn_Creature(self.player.opponent,threshold,life),self.player.opponent)
        self.room.env_mana(self.player,{"R":(2,5)},least_mana={"colorless":1,"R":2})
        return self.room.simulate_play(self.card,preferred_subactions=(1,))

    @simulate
    def simulate_power_5(self):
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
        threshold=self.card.effect_params["power_threshold"]
        life=max(self.card.effect_params["damage_low"],self.card.effect_params["damage_high"])+1
        self.stage_card(Testing_Spawn_Creature(self.player.opponent,max(0,threshold+1),life),self.player.opponent)
        self.room.env_mana(self.player,{"R":(2,5)},least_mana={"colorless":1,"R":2})
        return self.room.simulate_play(self.card,preferred_subactions=(1,))

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
        threshold=self.card.effect_params["power_threshold"]
        life=self.card.effect_params["damage_high"]
        self.stage_card(Testing_Spawn_Creature(self.player.opponent,threshold,life),self.player.opponent)
        self.room.env_mana(self.player,{"R":(2,5)},least_mana={"colorless":1,"R":2})
        return self.room.simulate_play(self.card,preferred_subactions=(1,))
