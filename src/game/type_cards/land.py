from typing import TYPE_CHECKING
import json
if TYPE_CHECKING:
    from game.player import Player




from game.card import Card
from game.type_action import actions
from game.game_function_tool import select_object
from game.buffs import Buff

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
        if self.get_flag("tap") or player.get_counter_from_dict("lands_summon_max")<=player.get_counter_from_dict("lands_summon"):
            return (False,"tap")
        else:
            return (True,"")
    

    def generate_mana(self)->dict:#返回一个dict{"R":1,"B":1}...
        return {}

    @select_object("",1)
    async def when_enter_battlefield(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        pass

    def when_leave_battlefield(self):
        pass

    def when_die(self):
        pass

    def when_sacrificed(self):#当牺牲时
        pass

    async def when_clicked(self,player:'Player'=None,opponent:'Player'=None):#当地牌被点击时横置，有一些是获得mana，有一些是别的能力   #启动式能力（Activated Abilities）：玩家可以在任何时候支付成本来使用的能力，通常格式为“[成本]：[效果]”。
        if not self.get_flag("tap"):
            
            mana=self.generate_mana()
            for key in mana:
                player.mana[key]+=mana[key]
            self.tap()
            #self.flag_dict["tap"]=True#横置
            return True
        else:
            return False
        
    def tap(self):
        if not self.get_flag("tap"):
            self.player.action_store.add_action(actions.Activate_Ability(self,self.player))
            self.flag_dict["tap"]=True#横置

    def untap(self):
        if self.get_flag("tap"):
            self.player.action_store.add_action(actions.Reset_Ability(self,self.player))
            self.flag_dict["tap"]=False#横置

    def check_ability_can_be_used(self,player:'Player'=None,opponent:'Player'=None):#有一些是“仅在你的回合”、“仅在主要阶段”、或“仅当堆栈为空时”能够激活
        return True

    async def when_play_this_card(self,player:'Player'=None,opponent:'Player'=None):# when player use the card
        await super().when_play_this_card(player, opponent)

       
        player.add_counter_dict("lands_summon",1)
        prepared_function=await self.when_enter_battlefield(player,opponent)
        if prepared_function=="cancel":
            return prepared_function
        player.remove_card(self,"hand")
        player.append_card(self,"land_area")
        return prepared_function

    def when_gain_buff(self,player: "Player" = None, opponent: "Player" = None,buff:Buff=None,card:'Card'=None):#当获得+1+1的buff时 OK
        self.player.action_store.start_record()
        
    
        
        self.player.action_store.add_action(actions.Add_Buff(card,self.player,self,"rgba(236, 230, 233, 0.8)","Missile_Hit",(),buff,True))
        self.player.action_store.end_record()

    def when_loss_buff(self,player: "Player" = None, opponent: "Player" = None,buff:Buff=None,card:'Card'=None):#当失去+1+1的buff时 OK
        self.player.action_store.start_record()

        self.player.action_store.add_action(actions.Lose_Buff(card,self.player,self,(),buff,True))
        self.player.action_store.end_record()

    def text(self,player:'Player',show_hide:bool=False)-> str:
        
        Flag_dict=f"str2json(string({json.dumps(self.flag_dict)}))"
        Counter_dict=f"str2json(string({json.dumps(self.counter_dict)}))"
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
        buffs=f"parameters({','.join([buff.text(player) for buff in self.buffs])})"
        return f"Land({Flag_dict},{Counter_dict},{Player},int({Id}),string({Name}),{Type},{Type_card},{Rarity},string({Content}),string({Image_Path}),state({result_mana}),{buffs})"


    def __repr__(self):
        content=f"({self.name},{self.type},{id(self)})"
        return content

