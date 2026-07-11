from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Shadowstrike.model import Shadowstrike

@bind_card(Shadowstrike)
class Shadowstrike_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Destroy target tapped creature. If a creature was destroyed this way, you may draw a card.",
        "[CARD_NAME] destroys target tapped creature; you may draw if one was destroyed.",
        "Destroy a tapped creature. Draw a card if a creature was destroyed.",
        "Choose target tapped creature. Destroy it. Optional draw.",
        "[CARD_NAME]: destroy tapped creature; optional draw.",
        "Eliminate target tapped creature. You may draw if destroyed.",
        "Destroy tapped creature. Draw if a creature dies this way.",
        "With [CARD_NAME], kill a tapped creature and maybe draw a card.",
        "Target tapped creature is destroyed. You may draw a card.",
        "[CARD_NAME] strikes tapped creatures; draw if one is destroyed.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.room.env_creature(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)
        for creature in self.player.battlefield+self.player.opponent.battlefield:
            creature.flag_dict["tap"]=True

        self.room.env_mana(
            self.player,
            {"B":(1,7)},
            least_mana={"colorless":2,"B":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
