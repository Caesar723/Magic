if __name__=="__main__":
    import sys
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/src")
    
    

from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_globals,guarded_getattr
import ast
import random

from game.type_cards.creature import Creature
from game.type_cards.instant import Instant
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object

class SandboxWrapper:
      def __init__(self, obj):
          self._obj = obj

      @property
      def cost(self):
          return self._obj.cost
      
      @property
      def type(self):
          return self._obj.type
      
      async def attact_to_object(self,object,power,color,type_missile):
          return await self._obj.attact_to_object(object,power,color,type_missile)
      
      async def cure_to_object(self,object,power,color,type_missile):
          return await self._obj.cure_to_object(object,power,color,type_missile)
      
      async def destroy_object(self,object,color,type_missile):
          return await self._obj.destroy_object(object,color,type_missile)
      
      async def exile_object(self,object,color,type_missile):
          return await self._obj.exile_object(object,color,type_missile)
      def get_flag(self,flag_name:str)->bool:
          return self._obj.get_flag(flag_name)
      
      def add_counter_dict(self,key:str,number:int)->None:# change the numebr of counter_dict
          self._obj.add_counter_dict(key,number)
      
      def set_counter_dict(self,key:str,number:int)->None:# change the numebr of counter_dict
          self._obj.set_counter_dict(key,number)
      
      def get_counter_from_dict(self,key:str):
          return self._obj.get_counter_from_dict(key)
      
      async def Scry(self,player,opponent,times):
          return await self._obj.Scry(player,opponent,times)

class PlayerSandboxWrapper:
    def __init__(self, obj):
        self._obj = obj

    @property
    def life(self):
        return self._obj.life
    
    @property
    def battlefield(self):
        return self._obj.battlefield
    
    @property
    def hand(self):
        return self._obj.hand
    
    @property
    def graveyard(self):
        return self._obj.graveyard
    
    @property
    def library(self):
        return self._obj.library
    
    @property
    def exile_area(self):
        return self._obj.exile_area
    
    @property
    def land_area(self):
        return self._obj.land_area
    
    def draw_card(self,number):
        return self._obj.draw_card(number)
    
    def remove_card(self,card,type):
        return self._obj.remove_card(card,type)
    
    def append_card(self,card,type):
        return self._obj.append_card(card,type)
    
    
    def get_manas(self):
        return self._obj.get_manas()
    
    def discard(self,card):
        return self._obj.discard(card)
    
    def send_selection_cards(self,selected_cards,selection_random):
        return self._obj.send_selection_cards(selected_cards,selection_random)
    
    def get_object(self,selected_cards,data):
        return self._obj.get_object(selected_cards,data)
    
    def check_can_use(self,cost):
        return self._obj.check_can_use(cost)
    
    async def generate_and_consume_mana(self,lands,cost,card):
        return await self._obj.generate_and_consume_mana(lands,cost,card)
    
    def get_flag(self,flag_name:str)->bool:
        return self._obj.get_flag(flag_name)
    
    def get_cards_by_pos_type(self,position:str,card_type:tuple["Creature|Land|Sorcery|Instant"],except_type:tuple["Creature|Land|Sorcery|Instant"]=()):
        return self._obj.get_cards_by_pos_type(position,card_type,except_type)
    
    
    
class SandboxCreatureWrapper(SandboxWrapper):
      def __init__(self, obj):
          super().__init__(obj)
      @property
      def state(self):
          return self._obj.state
      
      def tap(self):
          return self._obj.tap()
      
      def untap(self):
          return self._obj.untap()
      
class SandboxInstant_UndoWrapper(SandboxWrapper):
        def __init__(self, obj):
            super().__init__(obj)
        
        async def undo_stack(self,player,opponent):
            return await self._obj.undo_stack(player,opponent)
        

class SandboxLandWrapper(SandboxWrapper):
        def __init__(self, obj):
            super().__init__(obj)
        
        def tap(self):
            return self._obj.tap()
        
        def untap(self):
            return self._obj.untap()
        
def generate_creature_class(
        init_name:str,
        init_actual_live:int,
        init_actual_power:int,
        init_type_creature:str,
        init_type:str,
        init_mana_cost:str,
        init_color:str,
        init_type_card:str,
        init_rarity:str,
        init_content:str,
        init_image_path:str,
        select_object_range:str,
        when_enter_battlefield_function:str="",
        when_leave_battlefield_function:str="",
        when_die_function:str="",
        when_start_turn_function:str="",
        when_end_turn_function:str="",
        when_harm_is_done_function:str="",
        when_being_treated_function:str="",
        when_become_attacker_function:str="",
        when_become_defender_function:str="",
        when_kill_creature_function:str="",
        when_start_attcak_function:str="",
        when_start_defend_function:str="",
        when_a_creature_die_function:str="",
        when_an_object_hert_function:str="",
        aura_function:str="",
):
   
        
    class CreatureCard(Creature):
        def __init__(self,player):
            super().__init__(player)
            self.name=init_name
            self.live=init_actual_live
            self.power=init_actual_power
            self.actual_live=init_actual_live
            self.actual_power=init_actual_power
            self.type_creature=init_type_creature
            self.type=init_type
            self.mana_cost=init_mana_cost
            self.color=init_color
            self.type_card=init_type_card
            self.rarity=init_rarity
            self.content=init_content
            self.image_path=init_image_path

        async def get_user_code(self,function_code:str,player,opponent,creature=None,value=None,card=None):
            if not function_code:
                return True,None
            sandbox_globals = safe_globals.copy()
            sandbox_globals["getattr"] = guarded_getattr  # 替换 getattr
            sandbox_globals["setattr"] = None
            sandbox_globals["__builtins__"] = guarded_getattr(sandbox_globals["__builtins__"], "__dict__", {})
            sandbox_globals["self"] = SandboxCreatureWrapper(self)
            sandbox_globals["player"] = PlayerSandboxWrapper(player)
            sandbox_globals["opponent"] = PlayerSandboxWrapper(opponent)
            sandbox_globals["random"] = random
            if creature:
                sandbox_globals["creature"] = SandboxCreatureWrapper(creature)
            if value:
                sandbox_globals["value"] = value
            if card:
                sandbox_globals["card"] = card
            #print(sandbox_globals)
            try:
                async_code = f"async def user_code():\n    " + "\n    ".join(function_code.splitlines())
                parsed_code = ast.parse(async_code)
                compiled_code = compile(parsed_code, "<string>", "exec")  # 异步标志
                # 定义异步执行器
            
                exec(compiled_code, sandbox_globals)

                # 在异步上下文中运行代码
                user_code_func = sandbox_globals["user_code"]
                result = await user_code_func()
                success=True

                result = sandbox_globals.get("result", None)
            except Exception as e:
                print(e)
                success=False
                result=e
            return success,result


        
        @select_object(select_object_range,1)
        async def when_enter_battlefield(self,player,opponent,selected_object):
            success,result=await self.get_user_code(when_enter_battlefield_function,player,opponent,creature=selected_object)
            return result
        
        async def when_leave_battlefield(self,player= None, opponent = None,name:str='battlefield'):# when creature leave battlefield
            #await super().when_leave_battlefield(player,opponent,name)
            print(player,opponent)
            success,result=await self.get_user_code(when_leave_battlefield_function,player,opponent)
            print(success,result)
            return result
        
        async def when_die(self,player= None, opponent = None):# when creature die
            await super().when_die(player,opponent)
            success,result=await self.get_user_code(when_die_function,player,opponent)
            return result
        
        async def when_start_turn(self,player= None, opponent = None):# when creature start turn
            await super().when_start_turn(player,opponent)
            success,result=await self.get_user_code(when_start_turn_function,player,opponent)
            return result
        
        async def when_end_turn(self,player= None, opponent = None):# when creature end turn
            await super().when_end_turn(player,opponent)
            success,result=await self.get_user_code(when_end_turn_function,player,opponent)
            return result
        
        async def when_harm_is_done(self,card,value,player= None, opponent = None):# when creature harm is done
            await super().when_harm_is_done(card,value,player,opponent)
            success,result=await self.get_user_code(when_harm_is_done_function,player,opponent,card=card,value=value)
            return result
        
        async def when_being_treated(self,card,value,player= None, opponent = None):# when creature being treated
            await super().when_being_treated(card,value,player,opponent)
            success,result=await self.get_user_code(when_being_treated_function,player,opponent,card=card,value=value)
            return result
        
        async def when_become_attacker(self,player= None, opponent = None):# when creature become attacker
            await super().when_become_attacker(player,opponent)
            success,result=await self.get_user_code(when_become_attacker_function,player,opponent)
            return result
        
        async def when_become_defender(self,player= None, opponent = None):# when creature become defender
            await super().when_become_defender(player,opponent)
            success,result=await self.get_user_code(when_become_defender_function,player,opponent)
            return result
        
        async def when_kill_creature(self,card,player= None, opponent = None):# when creature kill creature
            await super().when_kill_creature(card,player,opponent)
            success,result=await self.get_user_code(when_kill_creature_function,player,opponent,card=card)
            return result
        
        async def when_start_attcak(self,card,player= None, opponent = None):# when creature start attcak
            await super().when_start_attcak(card,player,opponent)
            success,result=await self.get_user_code(when_start_attcak_function,player,opponent,card=card)
            return result
        
        async def when_start_defend(self,card,player= None, opponent = None):# when creature start defend
            await super().when_start_defend(card,player,opponent)
            success,result=await self.get_user_code(when_start_defend_function,player,opponent,card=card)
            return result
        
        async def when_a_creature_die(self,card,player= None, opponent = None):# when a creature die
            await super().when_a_creature_die(card,player,opponent)
            success,result=await self.get_user_code(when_a_creature_die_function,player,opponent,card=card)
            return result
        
        async def when_an_object_hert(self,card,value,player= None, opponent = None):# when an object hert
            await super().when_an_object_hert(card,value,player,opponent)
            success,result=await self.get_user_code(when_an_object_hert_function,player,opponent,card=card,value=value)
            return result
        
        async def aura(self,player= None, opponent = None):# when aura
            await super().aura(player,opponent)
            success,result=await self.get_user_code(aura_function,player,opponent)
            return result
        
        
        
        
        
        
        
        
        
        
        

            
    return CreatureCard

def generate_instant_class(
        init_name:str,
        init_type:str,
        init_mana_cost:str,
        init_color:str,
        init_type_card:str,
        init_rarity:str,
        init_content:str,
        init_image_path:str,
        select_object_range:str,
        is_undo:bool=False,
        card_ability_function:str="",
        when_a_creature_die_function:str="",
        when_an_object_hert_function:str="",
        when_kill_creature_function:str="",
        when_start_turn_function:str="",
        when_end_turn_function:str="",
        aura_function:str="",
):
    
        
    class InstantCard(Instant):
        def __init__(self,player):
            super().__init__(player)
            self.name=init_name
            self.type=init_type
            self.mana_cost=init_mana_cost
            self.color=init_color
            self.type_card=init_type_card
            self.rarity=init_rarity
            self.content=init_content
            self.image_path=init_image_path

        async def get_user_code(self,function_code:str,player,opponent,creature=None,value=None,card=None):
            if not function_code:
                return True,None
            sandbox_globals = safe_globals.copy()
            sandbox_globals["getattr"] = guarded_getattr  # 替换 getattr
            sandbox_globals["setattr"] = None
            sandbox_globals["__builtins__"] = guarded_getattr(sandbox_globals["__builtins__"], "__dict__", {})
            if is_undo:
                sandbox_globals["self"] = SandboxInstant_UndoWrapper(self)
            else:
                sandbox_globals["self"] = SandboxWrapper(self)
            sandbox_globals["player"] = PlayerSandboxWrapper(player)
            sandbox_globals["opponent"] = PlayerSandboxWrapper(opponent)
            sandbox_globals["random"] = random
            if creature:
                sandbox_globals["creature"] = SandboxCreatureWrapper(creature)
            if value:
                sandbox_globals["value"] = value
            if card:
                sandbox_globals["card"] = card
            #print(sandbox_globals)
            try:
                async_code = f"async def user_code():\n    " + "\n    ".join(function_code.splitlines())
                parsed_code = ast.parse(async_code)
                compiled_code = compile(parsed_code, "<string>", "exec")  # 异步标志
                # 定义异步执行器
            
                exec(compiled_code, sandbox_globals)

                # 在异步上下文中运行代码
                user_code_func = sandbox_globals["user_code"]
                result = await user_code_func()
                success=True

                result = sandbox_globals.get("result", None)
            except Exception as e:
                print(e)
                success=False
                result=e
            return success,result
        
        @select_object(select_object_range,1)
        async def card_ability(self,player,opponent,selected_object):
            success,result=await self.get_user_code(card_ability_function,player,opponent,selected_object=selected_object)
            return result
        
        async def when_a_creature_die(self,card,player= None, opponent = None):# when creature die
            await super().when_a_creature_die(card,player,opponent)
            success,result=await self.get_user_code(when_a_creature_die_function,player,opponent,card=card)
            return result
        
        async def when_an_object_hert(self,card,value,player= None, opponent = None):# when an object hert
            await super().when_an_object_hert(card,value,player,opponent)
            success,result=await self.get_user_code(when_an_object_hert_function,player,opponent,card=card,value=value)
            return result
        
        async def when_kill_creature(self,card,player= None, opponent = None):# when creature kill creature
            await super().when_kill_creature(card,player,opponent)
            success,result=await self.get_user_code(when_kill_creature_function,player,opponent,card=card)
            return result
        
        async def when_start_turn(self,player= None, opponent = None):# when creature start turn
            await super().when_start_turn(player,opponent)
            success,result=await self.get_user_code(when_start_turn_function,player,opponent)
            return result
        
        async def when_end_turn(self,player= None, opponent = None):# when creature end turn
            await super().when_end_turn(player,opponent)
            success,result=await self.get_user_code(when_end_turn_function,player,opponent)
            return result
        
        async def aura(self,player= None, opponent = None):# when aura
            await super().aura(player,opponent)
            success,result=await self.get_user_code(aura_function,player,opponent)
            return result
        
        
        
        

    return InstantCard


def generate_land_class(
        init_name:str,
        init_type:str,
        init_mana_cost:str,
        init_color:str,
        init_type_card:str,
        init_rarity:str,
        init_content:str,
        init_image_path:str,
        select_object_range:str,
        when_enter_battlefield_function:str="",
        when_clicked_function:str="",
        when_a_creature_die_function:str="",
        when_an_object_hert_function:str="",
        when_kill_creature_function:str="",
        when_start_turn_function:str="",
        when_end_turn_function:str="",
        aura_function:str="",
):
    
        
    class LandCard(Land):
        
        def __init__(self,player):
            super().__init__(player)
            self.name=init_name
            self.type=init_type
            self.mana_cost=init_mana_cost
            self.color=init_color
            self.type_card=init_type_card
            self.rarity=init_rarity
            self.content=init_content
            self.image_path=init_image_path
        
        async def get_user_code(self,function_code:str,player,opponent,creature=None,value=None,card=None):
            if not function_code:
                return True,None
            sandbox_globals = safe_globals.copy()
            sandbox_globals["getattr"] = guarded_getattr  # 替换 getattr
            sandbox_globals["setattr"] = None
            sandbox_globals["__builtins__"] = guarded_getattr(sandbox_globals["__builtins__"], "__dict__", {})
            
            sandbox_globals["self"] = SandboxLandWrapper(self)
            sandbox_globals["player"] = PlayerSandboxWrapper(player)
            sandbox_globals["opponent"] = PlayerSandboxWrapper(opponent)
            sandbox_globals["random"] = random
            if creature:
                sandbox_globals["creature"] = SandboxCreatureWrapper(creature)
            if value:
                sandbox_globals["value"] = value
            if card:
                sandbox_globals["card"] = card
            #print(sandbox_globals)
            try:
                async_code = f"async def user_code():\n    " + "\n    ".join(function_code.splitlines())
                parsed_code = ast.parse(async_code)
                compiled_code = compile(parsed_code, "<string>", "exec")  # 异步标志
                # 定义异步执行器
            
                exec(compiled_code, sandbox_globals)

                # 在异步上下文中运行代码
                user_code_func = sandbox_globals["user_code"]
                result = await user_code_func()
                success=True

                result = sandbox_globals.get("result", None)
            except Exception as e:
                print(e)
                success=False
                result=e
            return success,result
        @select_object(select_object_range,1)
        async def when_enter_battlefield(self,player= None, opponent = None):# when land enter battlefield
            await super().when_enter_battlefield(player,opponent)
            success,result=await self.get_user_code(when_enter_battlefield_function,player,opponent)
            return result
        
        async def when_clicked(self,player= None, opponent = None):# when land clicked
            #await super().when_clicked(player,opponent)
            success,result=await self.get_user_code(when_clicked_function,player,opponent)
            return result
        
        async def when_a_creature_die(self,card,player= None, opponent = None):# when a creature die
            await super().when_a_creature_die(card,player,opponent)
            success,result=await self.get_user_code(when_a_creature_die_function,player,opponent,card=card)
            return result
        
        async def when_an_object_hert(self,card,value,player= None, opponent = None):# when an object hert
            await super().when_an_object_hert(card,value,player,opponent)
            success,result=await self.get_user_code(when_an_object_hert_function,player,opponent,card=card,value=value)
            return result
        
        async def when_kill_creature(self,card,player= None, opponent = None):# when creature kill creature
            await super().when_kill_creature(card,player,opponent)
            success,result=await self.get_user_code(when_kill_creature_function,player,opponent,card=card)
            return result
        
        async def when_start_turn(self,player= None, opponent = None):# when creature start turn
            await super().when_start_turn(player,opponent)
            success,result=await self.get_user_code(when_start_turn_function,player,opponent)
            return result
        
        async def when_end_turn(self,player= None, opponent = None):# when creature end turn
            await super().when_end_turn(player,opponent)
            success,result=await self.get_user_code(when_end_turn_function,player,opponent)
            return result
        
        async def aura(self,player= None, opponent = None):# when aura
            await super().aura(player,opponent)
            success,result=await self.get_user_code(aura_function,player,opponent)
            return result
        
        
    return LandCard

def generate_sorcery_class(
        init_name:str,
        init_type:str,
        init_mana_cost:str,
        init_color:str,
        init_type_card:str,
        init_rarity:str,
        init_content:str,
        init_image_path:str,
        select_object_range:str,
        card_ability_function:str="",
        when_a_creature_die_function:str="",
        when_an_object_hert_function:str="",
        when_kill_creature_function:str="",
        when_start_turn_function:str="",
        when_end_turn_function:str="",
        aura_function:str="",
):
    class SorceryCard(Sorcery):
        
        def __init__(self,player):
            super().__init__(player)
            self.name=init_name
            self.type=init_type
            self.mana_cost=init_mana_cost
            self.color=init_color
            self.type_card=init_type_card
            self.rarity=init_rarity
            self.content=init_content
            self.image_path=init_image_path

        async def get_user_code(self,function_code:str,player,opponent,creature=None,value=None,card=None):
            if not function_code:
                return True,None
            sandbox_globals = safe_globals.copy()
            sandbox_globals["getattr"] = guarded_getattr  # 替换 getattr
            sandbox_globals["setattr"] = None
            sandbox_globals["__builtins__"] = guarded_getattr(sandbox_globals["__builtins__"], "__dict__", {})
            
            sandbox_globals["self"] = SandboxWrapper(self)
            sandbox_globals["player"] = PlayerSandboxWrapper(player)
            sandbox_globals["opponent"] = PlayerSandboxWrapper(opponent)
            sandbox_globals["random"] = random
            if creature:
                sandbox_globals["creature"] = SandboxCreatureWrapper(creature)
            if value:
                sandbox_globals["value"] = value
            if card:
                sandbox_globals["card"] = card
            #print(sandbox_globals)
            try:
                async_code = f"async def user_code():\n    " + "\n    ".join(function_code.splitlines())
                parsed_code = ast.parse(async_code)
                compiled_code = compile(parsed_code, "<string>", "exec")  # 异步标志
                # 定义异步执行器
            
                exec(compiled_code, sandbox_globals)

                # 在异步上下文中运行代码
                user_code_func = sandbox_globals["user_code"]
                result = await user_code_func()
                success=True

                result = sandbox_globals.get("result", None)
            except Exception as e:
                print(e)
                success=False
                result=e
            return success,result
        
        @select_object(select_object_range,1)
        async def card_ability(self,player= None, opponent = None,selected_object=None):# when sorcery card ability
            await super().card_ability(player,opponent,selected_object)
            success,result=await self.get_user_code(card_ability_function,player,opponent,selected_object=selected_object)
            return result
        
        async def when_a_creature_die(self,card,player= None, opponent = None):# when a creature die
            await super().when_a_creature_die(card,player,opponent)
            success,result=await self.get_user_code(when_a_creature_die_function,player,opponent,card=card)
            return result
        
        async def when_an_object_hert(self,card,value,player= None, opponent = None):# when an object hert  
            await super().when_an_object_hert(card,value,player,opponent) 
            success,result=await self.get_user_code(when_an_object_hert_function,player,opponent,card=card,value=value)
            return result
        
        async def when_kill_creature(self,card,player= None, opponent = None):# when creature kill creature
            await super().when_kill_creature(card,player,opponent)
            success,result=await self.get_user_code(when_kill_creature_function,player,opponent,card=card)
            return result
        
        async def when_start_turn(self,player= None, opponent = None):# when creature start turn
            await super().when_start_turn(player,opponent)
            success,result=await self.get_user_code(when_start_turn_function,player,opponent)
            return result
        
        async def when_end_turn(self,player= None, opponent = None):# when creature end turn
            await super().when_end_turn(player,opponent)
            success,result=await self.get_user_code(when_end_turn_function,player,opponent)
            return result
        
        async def aura(self,player= None, opponent = None):# when aura
            await super().aura(player,opponent)
            success,result=await self.get_user_code(aura_function,player,opponent)
            return result
        
    return SorceryCard


if __name__ == "__main__":
    import asyncio
    class_=generate_creature_class(
        "test",
        10,
        10,
        "Creature",
        "Creature",
        "1",
        "red", 
        "Creature",
        "Common",
        "",
        "",
        "",
        "",
"""
creature=random.choice(opponent.battlefield)
await self.exile_object(creature,"rgba(239, 228, 83, 0.8)","Missile_Hit")
""",
        
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",)
    from game.player import Player
    instance=class_(None)
    Player.action_processor="1"
    player1=Player("t1","",Player)
    player2=Player("t2","",Player)
    print(asyncio.run(instance.when_leave_battlefield(player1,player2,None)))