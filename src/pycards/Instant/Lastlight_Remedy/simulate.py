from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation
from pycards.Instant.Lastlight_Remedy.model import Lastlight_Remedy


@bind_card(Lastlight_Remedy)
class Lastlight_Remedy_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "If you have 8 or less life, you gain 8 life and draw a card. Otherwise, you gain 4 life.",
        "At 8 life or below, gain 8 life and draw one card; above 8 life, gain 4 life.",
        "If your life total is no greater than eight, restore eight life and draw a card. Otherwise restore four life."
    ]

    @simulate
    def simulate_life_7(self):
        self.basic_initinal({
            "graveyard":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(0,0)},
            "hand":{"creature_number":(0,1),"instant_number":(0,1),"sorcery_number":(0,1),"land_number":(0,1)},
            "library":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(6,8)},
        })
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)
        threshold=self.card.effect_params["life_threshold"]
        self.player.life=max(1,min(self.player.ini_life,threshold-1))
        self.room.env_mana(self.player,{"W":(2,5)},least_mana={"colorless":1,"W":2})
        return self.room.simulate_play(self.card,preferred_subactions=(0,))

    @simulate
    def simulate_life_8(self):
        self.basic_initinal({
            "graveyard":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(0,0)},
            "hand":{"creature_number":(0,1),"instant_number":(0,1),"sorcery_number":(0,1),"land_number":(0,1)},
            "library":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(6,8)},
        })
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)
        threshold=self.card.effect_params["life_threshold"]
        self.player.life=max(1,min(self.player.ini_life,threshold))
        self.room.env_mana(self.player,{"W":(2,5)},least_mana={"colorless":1,"W":2})
        return self.room.simulate_play(self.card,preferred_subactions=(0,))

    @simulate
    def simulate_life_9(self):
        self.basic_initinal({
            "graveyard":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(0,0)},
            "hand":{"creature_number":(0,1),"instant_number":(0,1),"sorcery_number":(0,1),"land_number":(0,1)},
            "library":{"creature_number":(0,0),"instant_number":(0,0),"sorcery_number":(0,0),"land_number":(6,8)},
        })
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)
        threshold=self.card.effect_params["life_threshold"]
        self.player.life=max(1,min(self.player.ini_life,threshold+1))
        self.room.env_mana(self.player,{"W":(2,5)},least_mana={"colorless":1,"W":2})
        return self.room.simulate_play(self.card,preferred_subactions=(0,))
