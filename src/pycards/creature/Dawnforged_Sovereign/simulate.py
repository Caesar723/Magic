from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation
from pycards.creature.Dawnforged_Sovereign.model import Dawnforged_Sovereign


@bind_card(Dawnforged_Sovereign)
class Dawnforged_Sovereign_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flying, vigilance. When [CARD_NAME] enters the battlefield, you gain 8 life and create two 2/2 white Knight creature tokens.",
        "Flying and vigilance. When [CARD_NAME] enters play, gain 8 life and summon two white 2/2 Knights.",
        "[CARD_NAME] has flying and vigilance; on entering the battlefield, it restores eight life to you and creates two 2/2 white Knight tokens."
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
        heal=self.card.effect_params["heal"]
        missing=random.choice((0,1,heal,heal+1,self.player.ini_life-1))
        self.player.life=max(1,self.player.ini_life-missing)

        self.room.env_mana(self.player,{"W":(4,7)},least_mana={"colorless":6,"W":4})
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
        heal=self.card.effect_params["heal"]
        missing=random.choice((0,1,heal,heal+1,self.player.ini_life-1))
        self.player.life=max(1,self.player.ini_life-missing)

        self.room.env_mana(self.player,{"W":(4,7)},least_mana={"colorless":6,"W":4})
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
        self.room.env_mana(self.player,{"W":(4,7)},least_mana={"colorless":6,"W":4})
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
        self.room.env_mana(self.player,{"W":(4,7)},least_mana={"colorless":6,"W":4})
        return self.room.simulate_creature_defend(self.card)
