from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation
from pycards.creature.Cryptwake_Colossus.model import Cryptwake_Colossus


@bind_card(Cryptwake_Colossus)
class Cryptwake_Colossus_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Lifelink. When [CARD_NAME] enters the battlefield, your opponent loses 3 life and you gain 3 life.",
        "Lifelink. When [CARD_NAME] enters play, the opposing player loses 3 life while you gain 3 life.",
        "[CARD_NAME] has lifelink; on entering the battlefield it drains three life from your opponent and restores three to you."
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
        heal=self.card.effect_params["heal"]
        missing=random.choice((0,1,heal,heal+1,self.player.ini_life-1))
        self.player.life=max(1,self.player.ini_life-missing)

        self.room.env_mana(self.player,{"B":(3,6)},least_mana={"colorless":4,"B":3})
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
        self.room.env_mana(self.player,{"B":(3,6)},least_mana={"colorless":4,"B":3})
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
        self.room.env_mana(self.player,{"B":(3,6)},least_mana={"colorless":4,"B":3})
        return self.room.simulate_creature_defend(self.card)
