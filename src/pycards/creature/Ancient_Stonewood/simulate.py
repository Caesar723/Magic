from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Ancient_Stonewood.model import Ancient_Stonewood

@bind_card(Ancient_Stonewood)
class Ancient_Stonewood_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Indestructible. Whenever [CARD_NAME] is dealt damage, it deals that much damage to a random creature an opponent controls.",

        "Indestructible. Each time [CARD_NAME] takes damage, it retaliates by dealing equal damage to a random opposing creature.",

        "Indestructible. When damage is dealt to [CARD_NAME], it strikes back for the same amount at a random enemy creature.",

        "Indestructible. If [CARD_NAME] is hurt, it mirrors that damage onto a random creature controlled by an opponent.",

        "Indestructible. Whenever [CARD_NAME] suffers damage, redirect that much damage to a random creature your opponent controls.",

        "Indestructible. Damage dealt to [CARD_NAME] causes it to deal an equal amount of damage to a random opposing creature.",

        "Indestructible. Each instance of damage to [CARD_NAME] triggers it to deal the same amount to a random enemy creature.",

        "Indestructible. When [CARD_NAME] is damaged, it lashes out and deals that much damage to a random creature an opponent controls.",

        "Indestructible. Any damage [CARD_NAME] receives is reflected back as equal damage to a random creature on the opposing battlefield.",

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
            {"U":(2,7)},
            least_mana={"colorless":4,"G":2}
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