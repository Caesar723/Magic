from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Shadow_Stalker.model import Shadow_Stalker

@bind_card(Shadow_Stalker)
class Shadow_Stalker_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Cannot be targeted by spells or abilities. Whenever [CARD_NAME] attacks, the opponent discards a card.",

        "Can't be targeted by spells or abilities. Whenever [CARD_NAME] attacks, the opponent discards a card.",

        "This can't be targeted by spells or abilities. Whenever [CARD_NAME] attacks, the opponent discards a card.",

        "Hexproof from spells and abilities. Whenever [CARD_NAME] attacks, the opponent discards a card.",

        "Immune to targeting by spells or abilities. Whenever [CARD_NAME] attacks, the opponent discards a card.",

        "Cannot be targeted by spells or abilities. Each time [CARD_NAME] attacks, the opponent discards a card.",

        "Cannot be targeted by spells or abilities. When [CARD_NAME] attacks, the opponent discards a card.",

        "Cannot be targeted by spells or abilities. On attack, [CARD_NAME] makes the opponent discard a card.",

        "Cannot be targeted by spells or abilities. Whenever [CARD_NAME] attacks, your opponent discards a card.",

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
            {"B":(2,7)},
            least_mana={"colorless":2,"B":2}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info

    @simulate
    def simulate_when_attack_opponent(self):
        self.basic_initinal()
        self.room.env_initinal_hand(
            self.player.opponent,
            {"land_number":(1,1)}
        )
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
