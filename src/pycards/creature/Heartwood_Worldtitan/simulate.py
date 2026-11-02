from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation
from pycards.creature.Heartwood_Worldtitan.model import Heartwood_Worldtitan


@bind_card(Heartwood_Worldtitan)
class Heartwood_Worldtitan_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Trample. When [CARD_NAME] enters the battlefield, create two 3/3 green Beast creature tokens.",
        "Trample. When [CARD_NAME] enters play, summon two green 3/3 Beasts.",
        "[CARD_NAME] has trample and creates two 3/3 green Beast tokens when it enters the battlefield."
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
        self.room.env_mana(self.player,{"G":(4,7)},least_mana={"colorless":6,"G":4})
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
        self.room.env_mana(self.player,{"G":(4,7)},least_mana={"colorless":6,"G":4})
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
        self.room.env_mana(self.player,{"G":(4,7)},least_mana={"colorless":6,"G":4})
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
        self.room.env_mana(self.player,{"G":(4,7)},least_mana={"colorless":6,"G":4})
        return self.room.simulate_creature_defend(self.card)
