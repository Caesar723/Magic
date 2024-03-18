from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player




from game.card import Card
from game.type_action import actions
from game.game_function_tool import select_object


class Land(Card):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.flag_dick:dict={}


    def check_can_use(self,player:'Player')->tuple[bool, str]:# check whether user can use this card , bool and reason
        return (True,"")
    

    def generate_mana(self)->dict:#返回一个dict{"R":1,"B":1}...
        return {}

    @select_object("",1)
    def when_enter_battlefield(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        pass

    def when_leave_battlefield(self):
        pass

    def when_die(self):
        pass

    def when_sacrificed(self):#当牺牲时
        pass

    def when_clicked(self,player:'Player'=None,opponent:'Player'=None):#当地牌被点击时横置，有一些是获得mana，有一些是别的能力   #启动式能力（Activated Abilities）：玩家可以在任何时候支付成本来使用的能力，通常格式为“[成本]：[效果]”。
        pass

    def check_ability_can_be_used(self,player:'Player'=None,opponent:'Player'=None):#有一些是“仅在你的回合”、“仅在主要阶段”、或“仅当堆栈为空时”能够激活
        return True

    async def when_play_this_card(self,player:'Player'=None,opponent:'Player'=None):# when player use the card
        await super().when_play_this_card(player, opponent)

        player.remove_card(self,"hand")
        player.append_card(self,"land_area")

        prepared_function=await self.when_enter_battlefield(player,opponent)
        return prepared_function


    def __repr__(self):
        content=f"({self.name},{self.type},{id(self)})"
        return content

