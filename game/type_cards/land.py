from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player




from game.card import Card
from game.type_action import actions
from game.game_function_tool import select_object


class Land(Card):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.flag_dict:dict={}



    def get_flag(self,flag_name:str):
        if flag_name in self.flag_dict:
            return self.flag_dict[flag_name]
        else:
            return False
        

    def check_can_use(self,player:'Player')->tuple[bool, str]:# check whether user can use this card , bool and reason
        if self.get_flag("tap"):
            return (False,"tap")
        else:
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
        if not self.get_flag("tap"):
            mana=self.generate_mana()
            for key in mana:
                player.mana[key]+=mana[key]
            self.flag_dict["tap"]=True#横置
            return True
        else:
            return False

    def check_ability_can_be_used(self,player:'Player'=None,opponent:'Player'=None):#有一些是“仅在你的回合”、“仅在主要阶段”、或“仅当堆栈为空时”能够激活
        return True

    async def when_play_this_card(self,player:'Player'=None,opponent:'Player'=None):# when player use the card
        await super().when_play_this_card(player, opponent)

        player.remove_card(self,"hand")
        player.append_card(self,"land_area")

        prepared_function=await self.when_enter_battlefield(player,opponent)
        return prepared_function

    def text(self,player:'Player',show_hide:bool=False)-> str:
        Flying=0
        Active=0
        Player=self.player.text(player)
        Id=id(self)
        if show_hide and player.name!=self.player.name:
            return f"Opponent({Player},int({Id}))"
        Name=self.name
        Type=self.color
        Type_card=self.type_card
        Rarity=self.rarity
        Content=self.content
        Image_Path=self.image_path

        manas=self.generate_mana()
        result_mana=[]
        for mana in ['U','W','B','R','G']:
            num=0
            if mana in manas:
                num=manas[mana]
            result_mana.append(str(num))
        result_mana=','.join(result_mana)
        print(result_mana)
        
        return f"Land({Flying},{Active},{Player},int({Id}),string({Name}),{Type},{Type_card},{Rarity},string({Content}),{Image_Path},state({result_mana}))"


    def __repr__(self):
        content=f"({self.name},{self.type},{id(self)})"
        return content

