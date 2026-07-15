from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Ralgar__the_Inferno_King__.model import Ralgar__the_Inferno_King__
from pycards.sorcery.Mystic_Insight.model import Mystic_Insight

@bind_card(Ralgar__the_Inferno_King__)
class Ralgar__the_Inferno_King___Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, it deals 3 damage to any target. Whenever you cast an instant or sorcery spell, [CARD_NAME] gets +1/+0 until end of turn.",

        "When [CARD_NAME] enters play, it deals 3 damage to any target. Whenever you cast an instant or sorcery, [CARD_NAME] gets +1/+0 until end of turn.",

        "As [CARD_NAME] enters the battlefield, it deals 3 damage to any target. Whenever you cast an instant or sorcery spell, [CARD_NAME] gets +1/+0 until end of turn.",

        "Upon entering the battlefield, [CARD_NAME] deals 3 damage to any target. Whenever you cast an instant or sorcery spell, [CARD_NAME] gets +1/+0 until end of turn.",

        "When [CARD_NAME] arrives, it deals 3 damage to any target. Whenever you cast an instant or sorcery spell, [CARD_NAME] gets +1/+0 until end of turn.",

        "When [CARD_NAME] enters the battlefield, deal 3 damage to any target. Whenever you cast an instant or sorcery spell, [CARD_NAME] gets +1/+0 until end of turn.",

        "When [CARD_NAME] enters the battlefield, it deals three damage to any target. Whenever you cast an instant or sorcery spell, [CARD_NAME] gets +1/+0 until end of turn.",

        "When [CARD_NAME] enters the battlefield, it deals 3 damage to any target. Each time you cast an instant or sorcery spell, [CARD_NAME] gets +1/+0 until end of turn.",

        "When [CARD_NAME] enters the battlefield, it deals 3 damage to any target. When you cast an instant or sorcery spell, [CARD_NAME] gets +1/+0 until end of turn.",

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
            {"R":(2,7)},
            least_mana={"colorless":3,"R":2}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info

    @simulate
    def simulate_when_attack_opponent(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
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

    @simulate
    def simulate_when_play_a_card(self):
        self.basic_initinal()
        self.random_life()(self.player)
        self.random_life()(self.player.opponent)
        self.stage_card(self.card)
        self.room.env_mana(
            self.player,
            {"U":(1,7)},
            least_mana={"colorless":1,"U":1}
        )

        trigger_card=Mystic_Insight(self.player)
        simulate_info=self.room.simulate_play(trigger_card)
        #simulate_info["card"]=self.card
        return simulate_info
