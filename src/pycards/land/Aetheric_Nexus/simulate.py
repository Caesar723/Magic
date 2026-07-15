from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Aetheric_Nexus.model import Aetheric_Nexus

@bind_card(Aetheric_Nexus)
class Aetheric_Nexus_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] enters the battlefield untapped and adds one colorless mana to your mana pool. You may also tap [CARD_NAME] to add one mana of any color, but only if you control a creature.",

        "[CARD_NAME] enters the battlefield untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color if you control a creature.",

        "When [CARD_NAME] enters the battlefield, it enters untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color, but only if you control a creature.",

        "[CARD_NAME] enters untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color if you control a creature.",

        "[CARD_NAME] enters the battlefield untapped and produces one colorless mana. You may tap [CARD_NAME] to add one mana of any color, but only if you control a creature.",

        "[CARD_NAME] enters the battlefield untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color while you control a creature.",

        "[CARD_NAME] enters untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color, but only if you have a creature on the battlefield.",

        "[CARD_NAME] enters the battlefield untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color if you have at least one creature.",

        "When [CARD_NAME] enters the battlefield untapped, add one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color, but only if you control a creature.",

        "[CARD_NAME] enters the battlefield untapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] to add one mana of any color, but only if you control at least one creature.",
    ]

    @simulate
    def simulate_with_controlled_creature(self):
        self.basic_initinal()
        # Its conditional mana mode is available only while its controller has a creature.
        self.room.env_creature(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (0, 3), "B": (0, 3), "G": (0, 3), "R": (0, 3), "W": (0, 3)},
        )

        return self.room.simulate_play(self.card)

    @simulate
    def simulate_activate_ability(self):
        self.basic_initinal()
        # generate_mana is enabled only while this land's controller has a creature.
        self.room.env_creature(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (0, 3), "B": (0, 3), "G": (0, 3), "R": (0, 3), "W": (0, 3)},
        )

        return self.room.simulate_activate_ability(self.card)
