from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation
from pycards.creature.Lord_of_the_Second_Grave.model import Lord_of_the_Second_Grave


@bind_card(Lord_of_the_Second_Grave)
class Lord_of_the_Second_Grave_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Lifelink. When [CARD_NAME] enters the battlefield, return all creature cards with mana value 3 or less from your graveyard to the battlefield.",
        "Lifelink. When [CARD_NAME] enters play, return every creature card costing 3 mana or less from your graveyard to play.",
        "[CARD_NAME] has lifelink. Its arrival returns all creature cards with mana value at most three from your graveyard to the battlefield."
    ]

    @simulate
    def simulate_empty_graveyard(self):
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
        self.room.env_mana(self.player,{"B":(4,7)},least_mana={"colorless":6,"B":4})
        return self.room.simulate_play(self.card,preferred_subactions=(0,))

    @simulate
    def simulate_mixed_graveyard(self):
        self.basic_initinal({
            "graveyard":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(0,0)},
            "hand":{"creature_number":(0,1),"instant_number":(0,1),"sorcery_number":(0,1),"land_number":(0,1)},
            "library":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(6,8)},
        })
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)
        from pycards.creature.Elite_Squire.model import Elite_Squire
        from pycards.creature.Storm_Bringer.model import Storm_Bringer
        self.room.env_no_creature(self.player)
        threshold=self.card.effect_params["mana_threshold"]
        for mana in (max(0,threshold-1),threshold):
            creature=Elite_Squire(self.player)
            creature.mana_cost=str(mana)
            self.stage_card(creature,zone="graveyard")
        creature=Storm_Bringer(self.player)
        creature.mana_cost=str(threshold+1)
        self.stage_card(creature,zone="graveyard")
        self.room.env_mana(self.player,{"B":(4,7)},least_mana={"colorless":6,"B":4})
        return self.room.simulate_play(self.card,preferred_subactions=(0,))

    @simulate
    def simulate_expensive_graveyard(self):
        self.basic_initinal({
            "graveyard":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(0,0)},
            "hand":{"creature_number":(0,1),"instant_number":(0,1),"sorcery_number":(0,1),"land_number":(0,1)},
            "library":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(6,8)},
        })
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)
        from pycards.creature.Storm_Bringer.model import Storm_Bringer
        self.room.env_no_creature(self.player)
        creature=Storm_Bringer(self.player)
        creature.mana_cost=str(self.card.effect_params["mana_threshold"]+1)
        self.stage_card(creature,zone="graveyard")
        self.room.env_mana(self.player,{"B":(4,7)},least_mana={"colorless":6,"B":4})
        return self.room.simulate_play(self.card,preferred_subactions=(0,))

    @simulate
    def simulate_when_attack(self):
        self.basic_initinal({
            "graveyard":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(0,0)},
            "hand":{"creature_number":(0,1),"instant_number":(0,1),"sorcery_number":(0,1),"land_number":(0,1)},
            "library":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(6,8)},
        })
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)
        self.room.env_mana(self.player,{"B":(4,7)},least_mana={"colorless":6,"B":4})
        return self.room.simulate_creature_attack(self.card)

    @simulate
    def simulate_when_defend(self):
        self.basic_initinal({
            "graveyard":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(0,0)},
            "hand":{"creature_number":(0,1),"instant_number":(0,1),"sorcery_number":(0,1),"land_number":(0,1)},
            "library":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(6,8)},
        })
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)
        self.room.env_one_creature(self.player.opponent)
        if not self.card.get_flag("flying") and not self.card.get_flag("reach"):
            self.player.opponent.battlefield[0].flag_dict["flying"]=False
        self.room.env_mana(self.player,{"B":(4,7)},least_mana={"colorless":6,"B":4})
        return self.room.simulate_creature_defend(self.card)
