from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Divine_Reckoning.model import Divine_Reckoning

@bind_card(Divine_Reckoning)
class Divine_Reckoning_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Destroy all non-angel creatures. Each player gains life equal to the number of creatures they controlled that were destroyed this way.",

        "[CARD_NAME] destroys all non-angel creatures. Each player gains life equal to the number of creatures they controlled that were destroyed this way.",

        "Destroy every creature that isn't an Angel. Each player gains life equal to the number of their creatures destroyed this way.",

        "[CARD_NAME] destroys all creatures except Angels. Each player gains life equal to the number of their creatures destroyed this way.",

        "All non-angel creatures are destroyed. Each player gains life equal to the number of creatures they controlled that were destroyed this way.",

        "[CARD_NAME] wipes all non-angel creatures. Each player gains life equal to how many of their creatures were destroyed this way.",

        "Destroy all creatures that are not Angels. Each player gains life equal to the number of their creatures destroyed this way.",

        "[CARD_NAME] destroys all non-angel creatures. Each player gains life equal to the count of their creatures destroyed this way.",

        "Every non-angel creature is destroyed. Each player gains life equal to the number of creatures they controlled that were destroyed this way.",

        "[CARD_NAME] destroys all non-angel creatures. Each player gains life equal to the number of their own creatures destroyed this way."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_creature(self.player)
        self.room.env_life_middle(self.player)
        self.room.env_creature(self.player.opponent)
        self.room.env_life_middle(self.player.opponent)
        for participant in (self.player,self.player.opponent):
            while len(participant.battlefield)<2:
                participant.battlefield.append(type(participant.battlefield[0])(participant))
            participant.battlefield[0].type_creature="Angel"
            for creature in participant.battlefield[1:]:
                creature.type_creature="Merfolk Creature"

        self.room.env_mana(
            self.player,
            {"W": (1, 7)},
            least_mana={"colorless": 4, "W": 1},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
