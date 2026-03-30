from typing import TYPE_CHECKING
import json
if TYPE_CHECKING:
    from game.player import Player




from game.card import Card
from game.type_action import actions
from game.game_function_tool import select_object,backup_instance_methods
from game.buffs import Buff
from game.game_function_tool import reset_instance_methods

class Land(Card):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.flag_dict:dict={}

        backup_instance_methods(self)



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
    async def when_enter_landarea(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        pass

    def die(self):
        self.flag_dict["die"]=True

    async def check_dead(self):#check whether land die,or whether appear at land area
        if self.get_flag("die"):
            return True
        else:
            return False

    def reset_to_orginal_state(self):
        reset_instance_methods(self)

    async def when_move_to_graveyard(self, player: "Player" = None, opponent: "Player" = None):#移入墓地 OK
        await self.when_die(player,opponent)
        await self.when_leave_landarea(player,opponent,'graveyard')
        self.reset_to_orginal_state()
        
        # player.remove_card(self,"battlefield")
        # player.append_card(self,"graveyard")

    async def when_leave_landarea(self,player: "Player" = None, opponent: "Player" = None,name:str='land_area'):# when creature leave battlefield
        player.remove_card(self,"land_area")
        player.append_card(self,name)

    async def when_die(self,player: "Player" = None, opponent: "Player" = None):#OK
        pass

    async def when_sacrificed(self,player: "Player" = None, opponent: "Player" = None):#当牺牲时
        pass

    async def sacrifice(self,color:str,type_missile:str):#当牺牲时
        self.flag_dict["die"]=True
        self.player.action_store.add_action(actions.Attack_To_Object(self,self.player,self,color,type_missile,(0,0)))
        await self.when_sacrificed(self.player,self.player.opponent)
        

    async def when_clicked(self,player:'Player'=None,opponent:'Player'=None,manual:bool=False):#当地牌被点击时横置，有一些是获得mana，有一些是别的能力   #启动式能力（Activated Abilities）：玩家可以在任何时候支付成本来使用的能力，通常格式为“[成本]：[效果]”。
        # Mana abilities only apply while the land is in its owner's land zone (not e.g. mis-zoned on battlefield).
        if self not in self.player.land_area:
            return False
        if not self.get_flag("tap"):
            self.player.add_counter_dict("spend_land_count",1)
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
        prepared_function=await self.when_enter_landarea(player,opponent)
        if prepared_function=="cancel":
            return prepared_function
        player.remove_card(self,"hand")
        player.append_card(self,"land_area")
        return prepared_function

    async def auto_play_this_card(self,player:'Player',opponent:'Player'):# when player use the card return prepared function
        self.player.action_store.start_record()
        await super().auto_play_this_card(player,opponent)
        prepared_function=await self.when_enter_landarea(player,opponent,auto_select=True)
        if prepared_function!="cancel":
            player.remove_card(self,"hand")
            player.append_card(self,"land_area")
            self.player.action_store.add_action(actions.Play_Cards(self,self.player))
        self.player.action_store.end_record()
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
        # print(result_mana)
        buffs=f"parameters({','.join([buff.text(player) for buff in self.buffs])})"
        return f"Land({Flag_dict},{Counter_dict},{Player},int({Id}),string({Name}),{Type},{Type_card},{Rarity},string({Content}),string({Image_Path}),state({result_mana}),{buffs})"


    def __repr__(self):
        content=f"({self.name},{self.type},{id(self)})"
        return content

