from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mystic_Reflection.model import Mystic_Reflection

@bind_card(Mystic_Reflection)
class Mystic_Reflection_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Choose target creature. If another creature with the same name is on the battlefield, transform that creature into a copy of the chosen creature until end of turn.",
        "[CARD_NAME] picks a creature; if another shares its name, that duplicate becomes a copy until end of turn.",
        "Choose a creature. Another creature with the same name becomes its copy until end of turn.",
        "With [CARD_NAME], select a creature and copy it onto another same-named creature this turn.",
        "Target a creature. Same-named creature on battlefield becomes a copy until end of turn.",
        "[CARD_NAME]: choose creature; duplicate same-named creature becomes copy until EOT.",
        "Pick a creature. If a same-named creature exists, it becomes a copy until end of turn.",
        "Choose target creature. Transform another same-named creature into its copy this turn.",
        "[CARD_NAME] makes a same-named creature a copy of your chosen creature until end of turn.",
        "Select a creature; another with the same name becomes a copy until end of turn.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.room.env_creature(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)
        # Whichever creature the action samples, another same-named creature exists.
        all_creatures=self.player.battlefield+self.player.opponent.battlefield
        shared_name=all_creatures[0].name
        for creature in all_creatures:
            creature.name=shared_name

        self.room.env_mana(
            self.player,
            {"U":(2,7)},
            least_mana={"colorless":1,"U":2}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
