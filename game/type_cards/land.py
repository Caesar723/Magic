from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player




from game.card import Card
from game.type_action import actions
from game.game_function_tool import select_object


class Land(Card):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.flag_dick:dict={}

    def generate_mana(self):
        pass

    @select_object("",1)
    def when_enter_battlefield(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        pass

    def when_leave_battlefield(self):
        pass

    def when_die(self):
        pass

    def when_sacrificed(self):#当牺牲时
        pass

    def when_clicked(self):#当地牌被点击时   #启动式能力（Activated Abilities）：玩家可以在任何时候支付成本来使用的能力，通常格式为“[成本]：[效果]”。
        pass

    def when_play_this_card(self,player:'Player'=None,opponent:'Player'=None):# when player use the card
        super().when_play_this_card(player, opponent)

        player.remove_card(self,"hand")
        player.append_card(self,"land_area")

        prepared_function=self.when_enter_battlefield(player,opponent)
        return prepared_function


    

