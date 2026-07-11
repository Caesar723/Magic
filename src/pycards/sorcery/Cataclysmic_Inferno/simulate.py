from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Cataclysmic_Inferno.model import Cataclysmic_Inferno

@bind_card(Cataclysmic_Inferno)
class Cataclysmic_Inferno_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals X damage to each creature your opponents control, where X is the number of Mountains you control. Then, for each creature destroyed this way, create a 1/1 red Elemental creature token with haste.",

        "Deal X damage to each creature your opponents control, where X is the number of Mountains you control. Then create a 1/1 red Elemental creature token with haste for each creature destroyed this way.",

        "[CARD_NAME] deals damage equal to the number of Mountains you control to each creature your opponents control. For each creature destroyed, create a 1/1 red Elemental token with haste.",

        "Each creature your opponents control takes X damage, where X is the number of Mountains you control. Then create a 1/1 red Elemental creature token with haste for each one destroyed.",

        "[CARD_NAME] hits each opponent's creature for X damage, where X is your Mountain count. For each creature destroyed, create a 1/1 red Elemental token with haste.",

        "Deal X damage to every creature your opponents control, where X equals the number of Mountains you control. Then create a 1/1 red Elemental token with haste for each creature destroyed.",

        "[CARD_NAME] deals X damage to opponent-controlled creatures, where X is the number of Mountains you control. Create a 1/1 red Elemental token with haste for each destroyed.",

        "Each creature your opponents control takes damage equal to the number of Mountains you control. For each creature destroyed this way, create a 1/1 red Elemental creature token with haste.",

        "[CARD_NAME] deals X damage to each creature your opponents control based on your Mountain count. Then create a 1/1 red Elemental token with haste for each creature destroyed.",

        "Deal damage equal to the number of Mountains you control to each creature your opponents control. Then create a 1/1 red Elemental creature token with haste for each creature destroyed this way."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_no_creature(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"R": (4, 7)},
            least_mana={"colorless": 3, "R": 1},
        )

        for creature in self.player.opponent.battlefield:
            creature.actual_live = min(creature.actual_live, 3)

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
