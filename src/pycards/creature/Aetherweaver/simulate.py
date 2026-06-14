from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Aetherweaver.model import Aetherweaver

@bind_card(Aetherweaver)
class Aetherweaver_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, examine the top three cards of your library. You may reveal an instant or sorcery card from among them and put it into your hand. Put the remaining cards on the bottom of your library in any order.",

        "When [CARD_NAME] enters the battlefield, look at the top three cards of your deck. You may choose an instant or sorcery card among them and add it to your hand. Put the rest on the bottom of your library in any order.",

        "Whenever [CARD_NAME] enters the battlefield, inspect the top three cards of your library. You may put an instant or sorcery card from among those cards into your hand. Place the remaining cards on the bottom of your library in any order.",

        "When [CARD_NAME] enters play, look through the top three cards of your library. You may take an instant or sorcery card from among them into your hand. Put the rest beneath your library in any order.",

        "As [CARD_NAME] enters the battlefield, view the top three cards of your library. You may select an instant or sorcery card from among them and put it into your hand. Put the remaining cards on the bottom of your deck in any order.",

        "When [CARD_NAME] enters the battlefield, reveal the top three cards of your library. You may put an instant or sorcery card revealed this way into your hand. Put the other cards on the bottom of your library in any order.",

        "When [CARD_NAME] enters the battlefield, check the top three cards of your library. You may place an instant or sorcery card from among them into your hand. Put the remaining cards on the bottom of your library in any order.",

        "When [CARD_NAME] enters the battlefield, search through the top three cards of your library. You may choose an instant or sorcery card among them and put it into your hand. Put the rest on the bottom of your library in any order.",

        "When [CARD_NAME] enters the battlefield, peek at the top three cards of your library. You may take an instant or sorcery card from among those cards into your hand. Put the remaining cards on the bottom of your library in any order.",

        "When [CARD_NAME] enters the battlefield, look at the top three cards of your library. You may reveal and put an instant or sorcery card from among them into your hand. Put the remaining cards on the bottom of your library in any order."
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
            {"U":(1,7)},
            least_mana={"colorless":2,"U":1}
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