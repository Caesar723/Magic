from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation
from pycards.sorcery.Ashen_Bargain.model import Ashen_Bargain


@bind_card(Ashen_Bargain)
class Ashen_Bargain_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Draw two cards, then you lose 2 life.",
        "Draw 2 cards. Afterward, lose 2 life.",
        "Take two cards from your library into your hand, then lose two life."
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
        self.room.env_mana(self.player,{"B":(1,4)},least_mana={"colorless":1,"B":1})
        return self.room.simulate_play(self.card,preferred_subactions=(0,))
