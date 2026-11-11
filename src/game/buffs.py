from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.card import Card
    from game.player import Player
    from game.type_cards.creature import Creature
    from game.type_action import actions


import types
import copy
import inspect



#setattr(instance, 方法名, property(new_func))如果是state要property的用property(new_func)，否则就直接用new_func
class Buff:
    
    def __init__(self,card:"Card",selected_card:"Card") -> None:
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str=""#这个buff是用在那个类型的
        self.content:str=""#描述buff
        self.buff_missile="Missile_Hit"
        self.color_missile="rgba(203, 203, 203, 0.9)"
        self.buff_name="Buff"
        self.selected_card=selected_card
        self.init_params = {
            "card": card,
            "selected_card": selected_card
        }

        
    
    def change_function(self,card:"Card"):
        pass
    
    def set_end_of_turn(self):
        
        self.selected_card.player.put_card_to_dict("end_step_buff",self)

    def when_end_turn(self):
        self.selected_card.loss_buff(self,self.card)
        
        self.selected_card.player.remove_card_from_dict("end_step_buff",self)

    def text(self,player):
        image_link=self.card.image_path
        content=self.content
        Id=id(self)
        Id_card=id(self.selected_card)
        return f"Buff(string({self.buff_name}),string({image_link}),string({content}),int({Id}),int({Id_card}))"


class StateBuff(Buff):
    def __init__(self,card:"Card",selected_card:"Card",power:int,live:int) -> None:
        super().__init__(card,selected_card)
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str="State"#这个buff是用在那个类型的
        unit=lambda num:"-" if num<0 else "+"
        self.content:str=f"{unit(power)}{power}/{unit(live)}{live}"#描述buff
        self.power=power
        self.live=live
        self.buff_name=f"{card.name}"
        self.init_params.update({
            "power": power,
            "live": live
        })

    def change_function(self,card:"Creature"):
        previews_func=card.calculate_state
        previews_func_take_damage=card.take_damage

        async def take_damage(self_card,card,value,player, opponent):# 可以受到来自各种卡牌的伤害
            if self.live>0:
                self.live-=value
                if self.live<=0:
                    value=-self.live
                    self.live=0
                else:
                    value=0
                    
            result=await previews_func_take_damage(card,value,player,opponent)
            return result

        def calculate_state(self_card):
            power,live=previews_func()
            power+=self.power
            live+=self.live
            return (power,live)
        card.calculate_state = types.MethodType(calculate_state, card)
        card.take_damage = types.MethodType(take_damage, card)

class KeyBuff(Buff):
    def __init__(self,card:"Card",selected_card:"Card",key_name:str) -> None:
        super().__init__(card,selected_card)
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str="Key"#这个buff是用在那个类型的
        
        self.content:str=f"{key_name}"#描述buff
        self.key_name=key_name
        self.buff_name=f"{card.name}"
        self.init_params.update({
            "key_name": key_name,
        })
    def change_function(self,card:"Creature"):
        previews_func=card.get_flag
        def get_flag(self_card,key):
            result=previews_func(key)
            if key==self.key_name:
                return True
            return result
        card.get_flag = types.MethodType(get_flag, card)

class Frozen(Buff):
    def __init__(self,card:"Card",selected_card:"Card") -> None:
        super().__init__(card,selected_card)
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str="Frozen"#这个buff是用在那个类型的
        self.content:str="frozen"#描述buff
        self.buff_name=f"{card.name}"
        self.set_end_of_turn()
        

    def change_function(self,card:"Creature"):
        previews_func=card.get_flag
        def get_flag(self_card,key):
            result=previews_func(key)
            if key=="tap":
                return True
            
            return result
        card.get_flag = types.MethodType(get_flag, card)
    
class Tap(Frozen):
    def __init__(self,card:"Card",selected_card:"Card") -> None:
        super().__init__(card,selected_card)
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str="Tap"#这个buff是用在那个类型的
        self.content:str="tap"#描述buff
        self.buff_name=f"{card.name}"
        self.set_end_of_turn()

    def change_function(self,card:"Creature"):
        previews_func=card.get_flag
        card.tap()
        def get_flag(self_card,key):
            result=previews_func(key)
            if key=="tap":
                return True
            
            return result
        
        def untap(self_card):
            pass
        card.get_flag = types.MethodType(get_flag, card)
        card.untap = types.MethodType(untap, card)
    def when_end_turn(self):
        super().when_end_turn()
        self.selected_card.untap()


class Indestructible(Buff):
    def __init__(self,card:"Card",selected_card:"Card") -> None:
        super().__init__(card,selected_card)
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str="Indestructible"#这个buff是用在那个类型的
        self.content:str="indestructible"#描述buff
        self.buff_name=f"{card.name}"

    def change_function(self,card:"Creature"):
        previews_func_flag=card.get_flag
        previews_func_take_damage=card.take_damage
        async def take_damage(self_card,card,value,player, opponent):# 可以受到来自各种卡牌的伤害
            power,live=self_card.state
            if live-value<=0:
                value=live-1
            result=await previews_func_take_damage(card,value,player,opponent)
            return result

        def get_flag(self_card,key):
            result=previews_func_flag(key)
            if key=="die":
                return False
            return result
        
        def die(self_card):
            pass
        card.get_flag = types.MethodType(get_flag, card)
        card.take_damage = types.MethodType(take_damage, card)
        card.die = types.MethodType(die, card)

class Infect(Buff):
    def __init__(self,card:"Card",selected_card:"Card") -> None:
        super().__init__(card,selected_card)
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str="Infect"#这个buff是用在那个类型的
        self.content:str="infect"#描述buff
        self.buff_name=f"{card.name}"

    def change_function(self, card: "Creature"):
        previews_func_deal=card.deal_damage
        previews_func_attact_to_object=card.attact_to_object
        async def deal_damage(self_card,card:"Creature",player: "Player" = None, opponent: "Player" = None):# 用在所有造成伤害的功能
            power,life=self_card.state

            buff=StateBuff(self_card,card,-power,-power)
            card.gain_buff(buff,self_card)
            rest_live=await card.take_damage(self_card,0,card.player,card.player.opponent) 
            
            
            await self_card.when_harm_is_done(card,power,player,opponent)
            if await card.check_dead():
                await self_card.when_kill_creature(card,player,opponent)
            return rest_live
        
        async def attact_to_object(self_card,object,power,color,type_missile):# it won't get hurt object can be card ot player

            if isinstance(object,(type(self_card.player),type(self_card.player.opponent))):
                # object.take_damage(self_card,power)
                # self_card.player.action_store.add_action(actions.Attack_To_Object(self_card,self_card.player,object,color,type_missile,[object.life]))
                # await object.check_dead()
                await previews_func_attact_to_object(object,power,color,type_missile)
            else:
                buff=StateBuff(self_card,object,-power,-power)
                object.gain_buff(buff,self_card)
                await previews_func_attact_to_object(object,0,color,type_missile)

        
        card.deal_damage = types.MethodType(deal_damage, card)
        card.attact_to_object = types.MethodType(attact_to_object, card)
        
class Clone(Buff):
    runtime_fields={"player","card_id","buffs","counter_dict","current_position","actual_power","actual_live",
                    "flag_dict","_original_methods","_active_clone","_clone_leaving"}
    runtime_flags={"tap","summoning_sickness","die","exile"}
    keyword_flags={"reach","Trample","flying","haste","Flash","lifelink","Vigilance","Menace","Hexproof",
                   "Islandwalk","Double strike","Defender","unblockable"}
    definition_fields=("name","type","type_card","type_creature","mana_cost","color","rarity","fixed_id",
                       "image_path","_content_template","extra_content","select_range")

    def __init__(self,card:"Card",selected_card:"Creature",reference_card:"Creature") -> None:
        super().__init__(card,selected_card)
        self.card_type="Clone"
        self.content=f"clone({reference_card.name})"
        self.buff_name=card.name
        self.reference_card=reference_card
        self.init_params.update({"reference_card":reference_card})
        self.prepare_copy(selected_card)

    @staticmethod
    def make_template(card_class,player):
        template=object.__new__(card_class)
        # Constructor buffs belong to the template and emit no gameplay actions.
        template.when_gain_buff=lambda *args,**kwargs:None
        card_class.__init__(template,player)
        template.__dict__.pop("when_gain_buff",None)
        return template

    @classmethod
    def values(cls,card):
        return {key:value for key,value in card.__dict__.items()
                if key not in cls.runtime_fields and not callable(value)}

    @staticmethod
    def copy_values(values):
        # Keep references to real game entities while giving the copy its own containers.
        return {key:value.copy() if isinstance(value,(dict,list,set)) else value for key,value in values.items()}

    @staticmethod
    def original_actual(card):
        actual=(card.actual_power,card.actual_live)
        active=card.__dict__.get("_active_clone")
        if active is None:
            return actual
        return tuple(active.saved_actual[i]+actual[i]-active.applied_actual[i] for i in range(2))

    def prepare_copy(self,card):
        reference=self.reference_card
        self.reference_class=type(reference)
        self.template=self.make_template(self.reference_class,card.player)
        self.copy_data=self.copy_values(self.values(self.template))
        for key in self.definition_fields:
            if key in reference.__dict__:
                self.copy_data[key]=reference.__dict__[key]
        self.copy_data=self.copy_values(self.copy_data)
        self.copy_data["effect_params"]=reference.effect_params.copy()
        self.copy_flags=self.template.flag_dict.copy()
        keys=self.keyword_flags|{buff.key_name for buff in reference.buffs if isinstance(buff,KeyBuff)}
        for key in keys:
            self.copy_flags[key]=reference.get_flag(key)
        self.state_reference=reference.state
        self.state_card=card.state
        self.base_actual=self.original_actual(card)
        actual=(card.actual_power,card.actual_live)
        self.state_bonus=tuple(self.state_card[i]-actual[i] for i in range(2))
        self.maximum_state=(reference.power+reference.state[0]-reference.actual_power,
                            reference.live+reference.state[1]-reference.actual_live)
        self.intrinsic_buffs=None

    def set_end_of_turn(self):
        self._end_turn_player=self.selected_card.player
        self._end_turn_player.put_card_to_dict("end_step_buff",self)

    def cancel_expiry(self):
        owner=getattr(self,"_end_turn_player",self.selected_card.player)
        owner.remove_card_from_dict("end_step_buff",self)

    def when_end_turn(self):
        self.cancel_expiry()
        self.selected_card.loss_buff(self,self.card)

    def change_function(self,card:"Creature"):
        from game.game_function_tool import backup_instance_methods

        if not hasattr(self,"copy_data"):
            self.prepare_copy(card)
            self.init_params["reference_card"]=self.reference_card
        self.saved_class=type(card)
        self.saved_data=self.values(card)
        self.saved_flags=card.flag_dict.copy()
        self.saved_methods=card._original_methods
        self.saved_actual=(card.actual_power,card.actual_live)
        original_template=self.make_template(type(card),card.player)
        intrinsic_types={type(buff) for buff in original_template.buffs}
        self.removed_buffs=[(index,buff) for index,buff in enumerate(card.buffs)
                            if type(buff) in intrinsic_types and buff.card is card and buff.selected_card is card]
        for _,buff in self.removed_buffs:
            card.buffs.remove(buff)
        for key in list(card.__dict__):
            if key in self.saved_data or callable(card.__dict__[key]):
                del card.__dict__[key]

        card.__class__=self.reference_class
        card.__dict__.update(self.copy_values(self.copy_data))
        card.flag_dict=self.copy_flags|{key:value for key,value in self.saved_flags.items() if key in self.runtime_flags}
        card.power=self.maximum_state[0]-self.state_bonus[0]
        card.live=self.maximum_state[1]-self.state_bonus[1]
        delta=tuple(self.saved_actual[i]-self.base_actual[i] for i in range(2))
        self.applied_actual=tuple(self.state_reference[i]-self.state_bonus[i]+delta[i] for i in range(2))
        card.actual_power,card.actual_live=self.applied_actual
        card._active_clone=self
        backup_instance_methods(card)

        if self.intrinsic_buffs is None:
            self.intrinsic_buffs=copy.deepcopy(self.template.buffs,{id(self.template):card,id(self.template.player):card.player})
        card.buffs.extend(self.intrinsic_buffs)

        for name in ("when_move_to_graveyard","when_move_to_exile_area"):
            method=getattr(card,name)

            async def leave(self_card,*args,_method=method,**kwargs):
                leaving=self_card.__dict__.get("_clone_leaving",False)
                self_card._clone_leaving=True
                try:
                    return await _method(*args,**kwargs)
                finally:
                    if leaving:
                        self_card._clone_leaving=True
                    else:
                        self_card.__dict__.pop("_clone_leaving",None)
                        if self_card not in self_card.player.battlefield:
                            self_card.clear_clone()

            setattr(card,name,types.MethodType(leave,card))

    def restore(self,card):
        # Preserve damage, healing and ability state through buff recalculation.
        actual=self.original_actual(card)
        self.copy_data=self.values(card)
        self.copy_flags={key:value for key,value in card.flag_dict.items() if key not in self.runtime_flags}
        flags=self.saved_flags|{key:value for key,value in card.flag_dict.items() if key in self.runtime_flags}
        for buff in self.intrinsic_buffs:
            if buff in card.buffs:
                card.buffs.remove(buff)
        for index,buff in self.removed_buffs:
            card.buffs.insert(min(index,len(card.buffs)),buff)
        for key in list(card.__dict__):
            if key not in self.runtime_fields or callable(card.__dict__[key]):
                del card.__dict__[key]
        card.__class__=self.saved_class
        card.__dict__.update(self.saved_data)
        card.actual_power,card.actual_live=actual
        card.flag_dict=flags
        card._original_methods=self.saved_methods
        card.__dict__.pop("_active_clone",None)
