from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Thunderclap_Behemoth.model import Thunderclap_Behemoth

@bind_card(Thunderclap_Behemoth)
class Thunderclap_Behemoth_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Trample. Whenever [CARD_NAME] attacks, it deals 3 damage to each creature defending player controls if you control another creature with power 4 or greater.",

        "Trample. Each time [CARD_NAME] attacks, it deals 3 damage to each creature defending player controls if you control another creature with power 4 or greater.",

        "Trample. When [CARD_NAME] attacks, it deals 3 damage to each creature defending player controls if you have another creature with power 4 or greater.",

        "Trample. On attack, [CARD_NAME] deals 3 damage to each creature defending player controls if you control another creature with power 4+.",

        "Trample. Whenever [CARD_NAME] attacks, if you control another creature with power 4 or greater, it deals 3 damage to each creature defending player controls.",

        "Trample. Whenever [CARD_NAME] attacks, it deals 3 damage to each defending creature if you control another creature with power 4 or greater.",

        "Trample. Whenever [CARD_NAME] attacks, it deals 3 damage to each creature the defending player controls if you control another creature with power 4 or greater.",

        "Trample. Whenever [CARD_NAME] attacks, it deals 3 damage to each creature defending player controls when you control another creature with power 4 or greater.",

        "Trample. Whenever [CARD_NAME] attacks, it deals 3 damage to each creature defending player controls if another creature you control has power 4 or greater.",

    ]
    @simulate
    def simulate_when_enter_battlefield(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"G":(2,7)},
            least_mana={"colorless":4,"G":2}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info

    @simulate
    def simulate_when_attack_opponent(self):
        self.basic_initinal()
        self.room.env_creature(self.player)
        for creature in self.player.battlefield:
            creature.power=max(creature.power,4)
            creature.actual_power=max(creature.actual_power,4)
        # simulate_creature_attack replaces one battlefield slot with this
        # card; keeping at least two slots guarantees another 4-power body.
        supporting_creature=type(self.card)(self.player)
        supporting_creature.power=max(supporting_creature.power,4)
        supporting_creature.actual_power=max(supporting_creature.actual_power,4)
        self.player.battlefield.append(supporting_creature)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U":(0,7),"B":(0,7),"G":(0,7),"R":(0,7),"W":(0,7)},
        )

        simulate_info=self.room.simulate_creature_attack(self.card)
        return simulate_info

    @simulate
    def simulate_when_defend_opponent(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U":(0,7),"B":(0,7),"G":(0,7),"R":(0,7),"W":(0,7)},
        )

        simulate_info=self.room.simulate_creature_defend(self.card)
        return simulate_info
