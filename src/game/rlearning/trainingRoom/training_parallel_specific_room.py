import sys
if __name__=="__main__":
    
    from pathlib import Path
    src_root = next(parent for parent in Path(__file__).resolve().parents if parent.name == "src")
    if str(src_root) not in sys.path:
        sys.path.append(str(src_root))
    
   
import inspect
import traceback
#from room_server import RoomServer
import numpy as np
import asyncio
import random
import os
import time
from multiprocessing import Process, Queue
from functools import partial

from game.type_action import actions
from game.train_agent import Agent_Train 
from game.room import Room

from game.rlearning.module.fixed_deck.ppo_agent import PPOTrainer
from game.base_agent_room import Base_Agent_Room
from game.rlearning.utils.model import get_class_by_name
from initinal_file import CARD_DICTION,CARD_SIMULATION_DICTION
from game.card import Card
from game.rlearning.utils.file import read_yaml
from game.type_cards.creature import Creature
from game.type_cards.instant import Instant
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery
from pycards.land.Mountain.model import Mountain
from pycards.land.Plains.model import Plains
from pycards.land.Island.model import Island
from pycards.land.Swamp.model import Swamp
from pycards.land.Forest.model import Forest
from game.testing_room import Testing_Spawn_Creature
from game.player import Player
from game.rlearning.trainingRoom.training_parallel_room import Multi_Agent_Parallel_Room
from game.rlearning.states.state_space.specific_entity import color_identity
from typing import TYPE_CHECKING
from game.game_function_tool import get_dir_names,name_replace,ORGPATH
import re
if TYPE_CHECKING:
    from game.rlearning.communicate.training_parallel_specific_room import Info_Communication
    from fastapi import WebSocket
    from game.card_simulation import Card_Simulation


CARD_AUGMENTATION_KEYWORDS = ("reach", "Trample", "flying", "haste", "Flash", "lifelink")


class Multi_Agent_Parallel_Specific_Room(Multi_Agent_Parallel_Room):

    CARDS_CACHE:dict[str,list[Card]]={}

    def __init__(self, env_config, info_communication:"Info_Communication", worker_id:int):
        self.env_config=env_config
        config_path=f"{ORGPATH}/{env_config['agent_config']}"
        config_path_list=[f"{ORGPATH}/{config_path}" for config_path in env_config["opponent_config"]]
        self.info_communication=info_communication
        self.worker_id=worker_id
        
        self.config_path=config_path
        self.config_path_list=config_path_list
        self.config=read_yaml(config_path)
        self.config_list=[read_yaml(config_path) for config_path in config_path_list]

        trainer1=get_class_by_name("game.rlearning.utils.baseAgent.EmptyTrainer")
        trainer1.pbar=None
        trainer_list=[get_class_by_name("game.rlearning.utils.baseAgent.EmptyTrainer") for config in self.config_list]
        self.agent1=trainer1(self.config,self.config["restore_step"],name="main")
        self.agent_list={
            config_path_list[i]:trainer(self.config_list[i],self.config_list[i]["restore_step"],name=f"agent{i+1}") 
            for i,trainer in enumerate(trainer_list)
        }

        Base_Agent_Room.__init__(self,None,None)
        self.action_process_condition=asyncio.Condition()#等待直到agent_cache不是空
        self.agent_cache=[]
        #store current player which is in his turn
        self.active_player:Agent_Train#进行操作的玩家
        self.non_active_player:Agent_Train
        
        
        Agent_Train.send_selection_cards.__defaults__=(True,True)
        Agent_Train.send_selection_cards.__defaults__=(True,True)

    def initinal_function(self,config:dict):
        result={}
        get_reward=get_class_by_name(config.get("reward_function","game.rlearning.rewards.win_base.get_reward"))
        result["get_reward"]=partial(get_reward,self)

        get_state=get_class_by_name(config.get("state_function","game.rlearning.states.fixed_deck.single_deck.get_state"))
        result["get_state"]=partial(get_state,self)


        action_transform_path=config.get("action_transform_function","game.rlearning.actions.fixed_deck.single_deck.num2action")
        num2action=get_class_by_name(action_transform_path)
        result["num2action"]=partial(num2action,self)

        action2num_path=config.get("action_inverse_transform_function",action_transform_path.replace("num2action","action2num"))
        action2num=get_class_by_name(action2num_path)
        result["action2num"]=partial(action2num,self)

        create_action_mask=get_class_by_name(config.get("action_mask_function","game.rlearning.actions.fixed_deck.single_deck.create_action_mask"))
        result["create_action_mask"]=partial(create_action_mask,self)

        return result

    def change_environmrnt(self):
        self.action_store_list_cache.clear()
        self.clear_environmrnt()
        

        card_simulation_cls=self.get_card_simulation()
        
        card_simulation:"Card_Simulation"=card_simulation_cls(self.player_1,self)
        self.augment_card_attributes(card_simulation.card)
        #print("simulate_card",card_simulation_cls.__name__)
        similar_description=card_simulation.get_similar_description()
        
        candidates=card_simulation.get_candidates_simulation()

        simulate_info=random.choice(candidates)()
        simulate_info["similar_description"]=similar_description

        for recorder_key in self.game_recorder:
            recorder=self.game_recorder[recorder_key]
            recorder.store_game_message(self.text(self.players[recorder_key]))

        return simulate_info

    def get_filtered_func(self,func_list:list[tuple],simulate_type:str):
        result=[]
        for func,types in func_list:
            if simulate_type in types:
                result.append(func)
        result=random.choice(result)
        return result

    def clear_environmrnt(self):
        self.flag_dict:dict={}
        self.counter_dict:dict={}
        self.attacker:Creature=None
        self.stack.clear()
        self.clear_player_environmrnt(self.player_1)
        self.clear_player_environmrnt(self.player_2)

    def clear_player_environmrnt(self,player):
        player.graveyard=[]
        player.hand=[]
        player.library=[]
        player.battlefield=[]
        player.life=20
        player.land_area=[]
        player.exile_area=[]
        player.treasure=[]
        player.counter_dict={}
        player.counter_dict["lands_summon_max"]=1
        player.flag_dict={}
        player.mana={"colorless":0,"U":0,"W":0,"B":0,"R":0,"G":0}
        player.cards_store_dict:dict[list]={}
        player.aura_pool:list[Card]=[]


    def get_cards_sample_by_name(self,name:str,number:int,is_except=False):
        if name == "undo":
            #print("get_cards_sample_by_name",name,number,is_except)
            result=[]
            types=["Instant","land","sorcery","creature"]
            subclass_dict={"Instant_Undo":"Instant"}
            class_dict={}
            for type in types:
                directory_path=f"{ORGPATH}/cards/{type}"
                for name in get_dir_names(directory_path):
                    class_name=name_replace(name)
                    class_dict[class_name]=name
            for subclass in Card.__subclasses__():
                for card in subclass.__subclasses__():
                    try:
                        class_name = re.sub(r'__$', '', card.__name__)
                        if class_name in subclass_dict:
                            if not is_except:
                                for subcard in card.__subclasses__():
                                    result.append(f"{class_dict[subcard.__name__]}_{subclass_dict[class_name]}")
                        else:
                            if is_except:
                                result.append(f"{class_dict[class_name]}_{subclass.__name__}")
                    except KeyError as e:
                        pass
            
        else:
            #print("get_cards_sample_by_name",name,number,is_except)
            if is_except:
                result=[
                    key for key in CARD_DICTION if name not in key.lower()
                ]
            else:
                result=[
                    key for key in CARD_DICTION if name in key.lower()
                ]
            
        # if name in self.CARDS_CACHE:
        #     return self.CARDS_CACHE[name]
        # else:
        #     self.CARDS_CACHE[name]=result
        result=random.sample(result,number)
        return result

    def get_card_simulation(self):
        return random.choice(list(CARD_SIMULATION_DICTION.values()))

    def augment_card_attributes(self,card:Card):
        """Randomly change one usable card attribute before scenario generation."""
        probability=self.config.get("card_attribute_augmentation_probability",0.0)
        if probability<=0.0 or random.random()>=probability:
            return
        costs=card.calculate_cost()
        choices=["cost"] if costs["colorless"] else []
        if isinstance(card,Creature):
            choices.extend(["state","base_state"])
            if any(not card.get_flag(keyword) for keyword in CARD_AUGMENTATION_KEYWORDS):
                choices.append("keyword")
        if not choices:
            return
        count=random.randint(1,min(3,len(choices)))
        selected=set(random.sample(choices,count))
        for choice in ("cost","base_state","state","keyword"):
            if choice not in selected:
                continue
            if choice=="cost":
                costs["colorless"]=random.randrange(costs["colorless"])
                colors="".join(color*costs[color] for color in ("U","W","B","R","G"))
                card.mana_cost=f"{costs['colorless'] or ''}{colors}"
            elif choice=="base_state":
                card.power=random.randint(1,8)
                card.live=random.randint(1,8)
                card.actual_power=card.power
                card.actual_live=card.live
            elif choice=="state":
                card.actual_power=random.randint(1,card.power)
                card.actual_live=random.randint(1,card.live)
            else:
                keyword=random.choice([key for key in CARD_AUGMENTATION_KEYWORDS if not card.get_flag(key)])
                card.flag_dict[keyword]=True
                if random.random()<0.5:
                    card.content=f"{card.content.rstrip('.')} {keyword}."


    def env_initinal_library(self,player,parameters:dict={}):
        cards=["Plains_Land","Island_Land","Swamp_Land","Mountain_Land","Forest_Land"]
        creature_number=parameters.get("creature_number",(0,0))
        instant_number=parameters.get("instant_number",(0,0))
        sorcery_number=parameters.get("sorcery_number",(0,0))
        land_number=parameters.get("land_number",(0,0))
        creature_cards=self.get_cards_sample_by_name("creature",random.randint(creature_number[0],creature_number[1]))
        instant_cards=self.get_cards_sample_by_name("instant",random.randint(instant_number[0],instant_number[1]))
        sorcery_cards=self.get_cards_sample_by_name("sorcery",random.randint(sorcery_number[0],sorcery_number[1]))
        land_cards=self.get_cards_sample_by_name("land",random.randint(land_number[0],land_number[1]))
        player.library=[
            CARD_DICTION[key](player)
            for key in creature_cards+instant_cards+sorcery_cards+land_cards+cards
        ]
        random.shuffle(player.library)

    
    def env_initinal_graveyard(self,player,parameters:dict={}):
        cards=["Plains_Land","Island_Land","Swamp_Land","Mountain_Land","Forest_Land"]
        creature_number=parameters.get("creature_number",(0,0))
        instant_number=parameters.get("instant_number",(0,0))
        sorcery_number=parameters.get("sorcery_number",(0,0))
        land_number=parameters.get("land_number",(0,0))
        creature_cards=self.get_cards_sample_by_name("creature",random.randint(creature_number[0],creature_number[1]))
        instant_cards=self.get_cards_sample_by_name("instant",random.randint(instant_number[0],instant_number[1]))
        sorcery_cards=self.get_cards_sample_by_name("sorcery",random.randint(sorcery_number[0],sorcery_number[1]))
        land_cards=self.get_cards_sample_by_name("land",random.randint(land_number[0],land_number[1]))
        player.graveyard=[
            CARD_DICTION[key](player)
            for key in creature_cards+instant_cards+sorcery_cards+land_cards+cards
        ]
        random.shuffle(player.graveyard)

    def env_initinal_hand(self,player,parameters:dict={}):
        creature_number=parameters.get("creature_number",(0,0))
        instant_number=parameters.get("instant_number",(0,0))
        sorcery_number=parameters.get("sorcery_number",(0,0))
        land_number=parameters.get("land_number",(0,0))
        creature_cards=self.get_cards_sample_by_name("creature",random.randint(creature_number[0],creature_number[1]))
        instant_cards=self.get_cards_sample_by_name("instant",random.randint(instant_number[0],instant_number[1]))
        sorcery_cards=self.get_cards_sample_by_name("sorcery",random.randint(sorcery_number[0],sorcery_number[1]))
        land_cards=self.get_cards_sample_by_name("land",random.randint(land_number[0],land_number[1]))

        player.hand=[
            CARD_DICTION[key](player)
            for key in creature_cards+instant_cards+sorcery_cards+land_cards
        ]
        random.shuffle(player.hand)
        

    def env_life_low(self,player):
        life=random.randint(1,7)
        player.life=life
        
    def env_life_middle(self,player):
        life=random.randint(8,14)
        player.life=life
        
    def env_life_high(self,player):
        life=random.randint(15,20)
        player.life=life
        

    def get_creature_sample(self, weight: float):
        """
        根据0~1的float权重生成一个随从样本，使用随机分配的方式，从总点数中抽取攻击和生命。
        flag数量略少且受权重影响较弱。
        """
        weight = max(0.0, min(weight, 1.0))
        flag_pool = [
            "flying", "trample", "haste", "first strike", "lifelink", "vigilance", "deathtouch", "hexproof", "reach"
        ]

        min_total_stat = 2     # 最低攻击+生命之和
        max_total_stat = 12    # 最高攻击+生命之和
        min_flags = 0
        max_flags = 1          # flag数量整体下调，最高只给1个

        # 总强度分配
        total_stat = int(round(min_total_stat + (max_total_stat - min_total_stat) * weight))
        flag_count = int(round(min_flags + (max_flags - min_flags) * weight))
        flag_count = max(0, min(flag_count, max_flags))

        # 至少分1点到攻击和生命
        remain_points = total_stat - 2
        points = [1, 1]  # 先给power和toughness各分1点
        # 剩余点数随机分配到power和toughness
        for _ in range(remain_points):
            idx = random.randint(0, 1)
            points[idx] += 1
        power, toughness = points
        current_toughness = toughness
        if toughness > 1 and random.random() < 0.4:
            current_toughness = random.randint(1, toughness - 1)

        chosen_flags = {}
        if flag_count > 0:
            sampled_flags = random.sample(flag_pool, flag_count)
            for key in sampled_flags:
                chosen_flags[key] = True

        return {
            "power": power,
            "toughness": toughness,
            "current_toughness": current_toughness,
            "flag_keywords": chosen_flags
        }


    
    def env_one_creature(self,player:"Player"):
        weight=random.random()
        creature_sample=self.get_creature_sample(weight)
        creature=Testing_Spawn_Creature(
            player,creature_sample["power"],creature_sample["toughness"],
            creature_sample["flag_keywords"],current_toughness=creature_sample["current_toughness"],
        )
        player.battlefield=[creature]

    def env_no_creature(self,player):
        player.battlefield=[]
    def env_creature(self,player:"Player"):
        num=random.randint(1,6)
        creatures=[]
        for i in range(num):
            weight=random.random()
            creature_sample=self.get_creature_sample(weight)
            creature=Testing_Spawn_Creature(
                player,creature_sample["power"],creature_sample["toughness"],
                creature_sample["flag_keywords"],current_toughness=creature_sample["current_toughness"],
            )
            creatures.append(creature)
        player.battlefield=creatures



    def env_mana(self,player:"Player",mana_range:dict[str,tuple[int,int]],least_mana:dict[str,tuple[int,int]]={}):
        player.mana={"colorless":0,"U":0,"W":0,"B":0,"R":0,"G":0}

        class_dict={
            "W":Plains,
            "U":Island,
            "B":Swamp,
            "R":Mountain,
            "G":Forest
        }
        temp_mana={"colorless":0,"U":0,"W":0,"B":0,"R":0,"G":0}
        for key in temp_mana:
            mana_range_min,mana_range_max=mana_range.get(key,(0,0))
            temp_mana[key]=random.randint(mana_range_min,mana_range_max)+temp_mana[key]
        colored_keys = ["U", "W", "B", "R", "G"]
        for key in colored_keys:
            need = least_mana.get(key, 0)
            if temp_mana[key] < need:
                temp_mana[key] = need
        colorless_need = least_mana.get("colorless", 0)
        colored_reserved = sum(least_mana.get(k, 0) for k in colored_keys)
        total_mana = sum(temp_mana.values())
        deficit = colorless_need - (total_mana - colored_reserved)
        if deficit > 0:
            all_keys = ["colorless"] + colored_keys
            for _ in range(deficit):
                temp_mana[random.choice(all_keys)] += 1
        player.mana["colorless"]=temp_mana["colorless"]
        for key in temp_mana:
            if key!="colorless":
                for _ in range(temp_mana[key]):
                    player.land_area.append(class_dict[key](player))

    def all_play_card_messages(self, player):
        name = player.name
        messages = []
        # sub_action=0: 无目标
        messages.append(f"{name}|play_card|0")
        sort_fn = self.create_sort_function(player)
        # sub_action 1-10: 敌方生物
        oppo_sorted = sorted(enumerate(player.opponent.battlefield), key=lambda x: sort_fn(x[1]), reverse=True)
        for rank in range(10):
            if rank < len(oppo_sorted):
                idx = oppo_sorted[rank][0]
                sel = f"{name}|field|opponent_battlefield|{idx}"
                messages.append(f"{name}|play_card|0||{sel}")
        # sub_action 11-20: 我方生物
        self_sorted = sorted(enumerate(player.battlefield), key=lambda x: sort_fn(x[1]), reverse=True)
        for rank in range(10):
            if rank < len(self_sorted):
                idx = self_sorted[rank][0]
                sel = f"{name}|field|self_battlefield|{idx}"
                messages.append(f"{name}|play_card|0||{sel}")
        # sub_action 21-22: 英雄
        messages.append(f"{name}|play_card|0||{name}|field|oppo|")
        messages.append(f"{name}|play_card|0||{name}|field|self|")
        # sub_action 23-32: 选手牌
        for card_idx in range(12, 22):
            sel = f"{name}|cards|{card_idx}|"
            messages.append(f"{name}|play_card|0||{sel}")
        return messages

    def env_stack_cards(
        self,
        player: "Player",
        undo_card: Instant = None,
        preferred_types: tuple[str, ...] = None,
        max_mana_value: int = None,
    ):
        """Build a resolvable stack for an ``Instant_Undo`` simulation.

        The card on top is always controlled by the opponent and, when an undo
        card is supplied, matches that card's ``undo_range``.  Stack cards are
        also staged in the zone used by the real play flow so counter effects
        that move the countered card do not fail during resolution.
        """
        self.stack.clear()

        async def empty_prepared_function():
            return None

        def normalize_type(card_type: str) -> str:
            return card_type.lower()

        def card_keys_for(card_types: list[str]) -> list[str]:
            normalized = {normalize_type(card_type) for card_type in card_types}
            return [
                key
                for key in CARD_DICTION
                if key.rsplit("_", 1)[-1].lower() in normalized
            ]

        def create_card(
            owner: "Player",
            card_types: list[str],
            mana_value_limit: int = None,
        ) -> Card:
            keys = card_keys_for(card_types)
            random.shuffle(keys)
            for key in keys:
                candidate = CARD_DICTION[key](owner)
                if mana_value_limit is None or sum(candidate.cost.values()) <= mana_value_limit:
                    return candidate
            raise ValueError(
                f"No stack card matches types={card_types} and "
                f"max_mana_value={mana_value_limit}"
            )

        def stage_stack_card(card: Card):
            owner = card.player
            if isinstance(card, Creature):
                owner.battlefield.append(card)
            elif isinstance(card, Land):
                owner.land_area.append(card)
            else:
                owner.graveyard.append(card)

            self.stack.append({
                "card": card,
                "prepared_function": empty_prepared_function,
                "message": random.choice(self.all_play_card_messages(owner)),
            })

        # Lower stack entries make multi-counter effects meaningful while the
        # final entry below remains the guaranteed legal target.
        lower_count = random.randint(0, 3)
        if undo_card is not None and type(undo_card).__name__ == "Time_Reversal":
            lower_count = random.randint(1, 3)
        for _ in range(lower_count):
            owner = random.choice([player, player.opponent])
            card = create_card(owner, ["instant", "sorcery"])
            stage_stack_card(card)

        if undo_card is None or getattr(undo_card, "undo_range", "all") == "all":
            allowed_types = ["creature", "instant", "sorcery"]
        else:
            allowed_types = [
                normalize_type(card_type)
                for card_type in undo_card.undo_range.split("|")
            ]

        if preferred_types:
            preferred = [normalize_type(card_type) for card_type in preferred_types]
            target_types = [card_type for card_type in preferred if card_type in allowed_types]
            if not target_types:
                raise ValueError(
                    f"preferred_types={preferred_types} do not match "
                    f"undo_range={getattr(undo_card, 'undo_range', 'all')}"
                )
        else:
            target_types = allowed_types

        target_card = create_card(player.opponent, target_types, max_mana_value)
        stage_stack_card(target_card)



    def choose_card(self,constraint:dict):
        if constraint.get("battlefield",None):
            return self.get_cards_sample_by_name("creature",1)[0]
        if constraint.get("hand",None):
            return self.get_cards_sample_by_name("undo",1,True)[0]
        
        
    def sample_action(self,action_range:tuple[int,int]):
        # 从 mask 里抽一个为 true index，但是有范围限制
        
        actions_mask = self.basic_func[self.player_1.name]["create_action_mask"](self.player_1)[0]
        #print(actions_mask)
        min_index,max_index = action_range  # 设置你想要的最大index（不包含max_index本身）
        actions = [i for i in range(min_index, max_index) if actions_mask[i]]
        if not actions:
            return None
        action = random.choice(actions)
        return action

    def sample_card_action(self,card_index:int,preferred_subactions=None):
        start=32+card_index*33
        if preferred_subactions is None:
            return self.sample_action((start,start+33))

        actions_mask=self.basic_func[self.player_1.name]["create_action_mask"](self.player_1)[0]
        actions=[
            start+sub_action
            for sub_action in preferred_subactions
            if 0<=sub_action<33 and actions_mask[start+sub_action]
        ]
        return random.choice(actions) if actions else None

        
    
    def simulate_play(self,card:Card,preferred_subactions=None):
        
        card.flag_dict["tap"]=False
        if self.player_1.hand and len(self.player_1.hand)!=1:
            card_index=min(9,random.randint(0,len(self.player_1.hand)-1))
            self.player_1.hand[card_index]=card
        else:
            self.player_1.hand.append(card)
            card_index=len(self.player_1.hand)-1
        self.active_player=self.player_1
        self.non_active_player=self.player_2

        instance_dict={
            Creature:"when_enter_battlefield",
            Instant:"card_ability",
            Land:"when_enter_landarea",
            Sorcery:"card_ability"
        }
        select_dict={
            'all_roles':[self.player_2,self.player_1],
            'opponent_roles':[self.player_2], 
            'your_roles':[self.player_1],
            'all_creatures':[self.player_2,self.player_1],
            'opponent_creatures':[self.player_2],
            'your_creatures':[self.player_1],
        }
        land_select_dict={
            'all_lands':[self.player_2,self.player_1],
            'opponent_lands':[self.player_2],
            'your_lands':[self.player_1],
        }
        
        for cls in instance_dict:
            if isinstance(card,cls):
                select_range=getattr(card,instance_dict[cls]).select_range
        if select_range in select_dict:
            for player in select_dict[select_range]:
                if not player.battlefield:
                    self.env_creature(player)
        elif select_range in land_select_dict:
            for player in land_select_dict[select_range]:
                if not player.land_area:
                    player.land_area.append(Plains(player))


        action=self.sample_card_action(card_index,preferred_subactions)

        simulate_info={
            "card":card,
            "type":0,
            "action":action
        }
        #(simulate_info)

        return simulate_info

    
    def simulate_play_in_stack(self,card:Card,preferred_subactions=None):
        self.flag_dict["bullet_time"]=True

        card.flag_dict["tap"]=False
        if self.player_1.hand and len(self.player_1.hand)!=1:
            card_index=min(9,random.randint(0,len(self.player_1.hand)-1))
            self.player_1.hand[card_index]=card
        else:
            self.player_1.hand.append(card)
            card_index=len(self.player_1.hand)-1
        self.active_player=self.player_1
        self.non_active_player=self.player_2

        instance_dict={
            Creature:"when_enter_battlefield",
            Instant:"card_ability",
            Land:"when_enter_landarea",
            Sorcery:"card_ability"
        }
        select_dict={
            'all_roles':[self.player_2,self.player_1],
            'opponent_roles':[self.player_2], 
            'your_roles':[self.player_1],
            'all_creatures':[self.player_2,self.player_1],
            'opponent_creatures':[self.player_2],
            'your_creatures':[self.player_1],
        }
        land_select_dict={
            'all_lands':[self.player_2,self.player_1],
            'opponent_lands':[self.player_2],
            'your_lands':[self.player_1],
        }
        
        for cls in instance_dict:
            if isinstance(card,cls):
                select_range=getattr(card,instance_dict[cls]).select_range
        if select_range in select_dict:
            for player in select_dict[select_range]:
                if not player.battlefield:
                    self.env_creature(player)
        elif select_range in land_select_dict:
            for player in land_select_dict[select_range]:
                if not player.land_area:
                    player.land_area.append(Plains(player))

        action=self.sample_card_action(card_index,preferred_subactions)

        simulate_info={
            "card":card,
            "type":0,
            "action":action
        }
        #print(simulate_info)

        return simulate_info

    def simulate_activate_ability(self,card:Card):
        card.flag_dict["tap"]=False

        # ``specific.get_state`` currently exposes aggregate mana but not the
        # ordered land zone.  Keep the supervised activation label stable at
        # slot zero instead of assigning an unobservable random land index.
        card_index=0
        if self.player_1.land_area:
            old_card=self.player_1.land_area[card_index]
            for key in old_card.check_overwritten():
                self.player_1.remove_card_from_dict(key,old_card)
            self.player_1.land_area[card_index]=card
        else:
            self.player_1.land_area.append(card)
        for key in card.check_overwritten():
            self.player_1.put_card_to_dict(key,card)
        self.active_player=self.player_1
        self.non_active_player=self.player_2

        action=self.sample_action((22+card_index,22+card_index+1))

        simulate_info={
            "card":card,
            "type":0,
            "action":action
        }
        #print(simulate_info)

        return simulate_info

    def simulate_creature_attack(self,card:Card):
        if self.player_1.battlefield and len(self.player_1.battlefield)!=1:
            card_index=min(9,random.randint(0,len(self.player_1.battlefield)-1))
            self.player_1.battlefield[card_index]=card
        else:
            self.player_1.battlefield.append(card)
            card_index=len(self.player_1.battlefield)-1
        if card.get_flag("Double strike"):
            card.set_counter_dict("attack_counter",2)
        else:
            card.set_counter_dict("attack_counter",1)
        card.flag_dict["summoning_sickness"]=False
        card.flag_dict["tap"]=False
        self.flag_dict["attacker_defenders"]=False
        
        self.active_player=self.player_1
        self.non_active_player=self.player_2


        action=self.sample_action((2+card_index,2+card_index+1))

        simulate_info={
            "card":card,
            "type":1,
            "action":action
        }

        return simulate_info

    def simulate_creature_defend(self,card:Card):
        self._elapsed_time=time.perf_counter()
        
        card.flag_dict["tap"]=False
        if self.player_1.battlefield and len(self.player_1.battlefield)!=1:
            card_index=min(9,random.randint(0,len(self.player_1.battlefield)-1))
            self.player_1.battlefield[card_index]=card
        else:
            self.player_1.battlefield.append(card)
            card_index=len(self.player_1.battlefield)-1
        card.flag_dict["summoning_sickness"]=False
        self.flag_dict["attacker_defenders"]=True
        opponent_card=random.choice(self.player_2.battlefield)
        self.attacker=opponent_card
        self.active_player=self.player_2
        self.non_active_player=self.player_1


        action=self.sample_action((12+card_index,12+card_index+1))

        simulate_info={
            "card":card,
            "type":2,
            "action":action
        }
        return simulate_info

    async def action_process_system(self):#这个会等待，直到收到send_actioin_request发送的请求
        repeat_train=True
        while repeat_train:
            #print(self)
            

            for i in range(256):
                simulate_info=self.change_environmrnt()
                #print(self)
                #print(simulate_info)
                action=simulate_info["action"]
                if action is None:
                    continue
                agent:Agent_Train=self.player_1
                state=self.basic_func[agent.name]["get_state"](agent)
                state["card_used"]=self.get_card_used_info(simulate_info)

                #print(action)
                
                reward_func=await self.process_action(agent,action)
                #print(self)

                # print("\n\n\n\n\n")
                #asyncio.create_task(agent.store_data(state,action,reward_func))
                
                #print(self)
                oppo_agent:Agent_Train=agent.opponent

                #print(agent.name,mask,action)
                if agent==self.player_1:
                    
                    if action!=0:
                        await agent.store_data(state,action,reward_func)
                    else:
                        #print("store_data_func",action)
                        
                        async def store_data_func(agent=agent,state=state,action=action,reward_func=reward_func):
                            #print("store_data_func",action,id(store_data_func),id(reward_func),id(state))
                            await agent.store_data(state,action,reward_func)
                        #print("store_data_func",action,id(store_data_func),id(reward_func),id(state))
                        agent.add_pedding_store_task(store_data_func)
                        #print(len(agent.pedding_store_task))
                    
                await self.check_death()
                
            
            self.send_data_to_host(agent if agent==self.player_1 else oppo_agent)
            #print("finish")
            self.gamming=True
            await self.initinal_environmrnt()
            
            
        #self.active_player.update()

    def get_card_used_info(self,simulate_info:dict):
        card=simulate_info["card"]
        similar_description=simulate_info["similar_description"]
        card_type,card_special_type=self.get_card_special_types(card)
        max_mana=20
        max_state=20
        card_manas=[]
        for mana in list(card.calculate_cost().values()):
            mana=max(0,min(max_mana,int(mana)))
            # mana_one_hot=np.zeros(max_mana)
            # mana_one_hot[mana]=1
            card_manas.append(mana/max_mana)
        if card_type==1:
            has_state=1
            attack,defend=list(card.state)
            
        else:
            has_state=0
            attack=defend=0


        return {
            "description":card.content,
            "similar_description":similar_description,
            "special_type":card_special_type,
            "mana_cost":np.array(card_manas),
            "color_identity":color_identity(card.mana_cost, getattr(card, "color", ""), card.name),
            "attack":attack/max_state,
            "defend":defend/max_state,
            "has_state":has_state,
            "card_type":card_type,
        }

    def send_data_to_host(self,agent:Agent_Train):


        self.info_communication.store_game_data(agent.agent.dataset.datas)
        agent.agent.dataset.datas = []
    
        

    async def game_end(self,died_player:list[Agent_Train]):
        self.gamming=False
       
        for player in [self.player_1,self.player_2]:
            await player.clear_pedding_store_task()




    async def process_action(self,agent:Agent_Train,action:int)->tuple:
        #将action 处理生成动作并且传入房间，将其挂起，直到房间处理好请求收到结束信号
        #如果是攻击的action，给敌方agent发送动作请求，自己挂起再一次，直到地方action动作做好发送信息给自己，自己结束挂起，计算state
        # 获取state，done，计算reward
        #返回new state 和 reward 和 done
        message:str=await self.basic_func[agent.name]["num2action"](agent,action)
        #print(message)
        username,type,content=message.split("|")
        #old_reward=self.get_reward_red(agent)
        #print(username,content,type)
        old_rewards=self.basic_func[agent.name]["get_reward"](agent)
        info_index=len(self.game_recorder[agent.name].datas)
        old_reward=old_rewards["reward"]

        if action==1 or (action>=12 and action <=21):
            attacker=self.attacker
            
        else:
            attacker=None
        if action>=2 and action <=21:
            
            selected_creature=agent.battlefield[int(content)]
        else:
            selected_creature=None
        await self.message_process_dict[type](username,content)
        await self.check_death()


        if action>=2 and action <=11:
            
            agent_oppo:Agent_Train=agent.opponent
            state=self.basic_func[agent_oppo.name]["get_state"](agent_oppo)
            mask=self.basic_func[agent_oppo.name]["create_action_mask"](agent_oppo)
            state["mask"]=mask

            min_index,max_index = (12,22)  # 设置你想要的最大index（不包含max_index本身）
            actions = [i for i in range(min_index, max_index) if mask[0][i]]+[1]
            if not actions:
                return None
            action_oppo = random.choice(actions)
            await self.process_action(agent_oppo,action_oppo)

        elif action>=22 and action <=31:
            pass
            
        elif action!=0:
            await self.end_bullet_time()
        elif action==0:
            # async def zero_reward_func():
            #     return state,0,False
            #agent.notify_reward=False

            flag=True

        
        #change_reward=new_reward-old_reward

        async def next_state_function(info_index=info_index):
            
            current_rewards=self.basic_func[agent.name]["get_reward"](agent,selected_creature,attacker)
            current_reward=current_rewards["reward"]
            # if action==0:
            #     new_reward=0
            # else:
                
            new_reward=current_reward-old_reward
            new_reward/=5
            if action==0:
                info_index=len(self.game_recorder[agent.name].datas)
                new_reward/=50
            

            if self.config.get("long_sight",False):
                if action>=2 and action <=11:
                    new_reward=0
                if action==0:
                    new_reward=0
                #new_reward*=5
                
            new_reward=max(min(new_reward,0.3),-0.3)
            #await self.check_death()
            die_player=await self.check_player_die()
            
            done=False
            
            if die_player and agent.life<=0:
                
                new_reward=-1
                done=True

                #if flag:
                # print("lose",action,message,agent.life,org_state,self,self.gamming,new_reward)
                # print("traceback.format_stack():")
                # print("".join(traceback.format_stack()))
            elif die_player:
                
                new_reward=1
                done=True
                # print("win",action,message,agent.life,org_state,self,self.gamming,new_reward)
                # print("traceback.format_stack():")
                # print("".join(traceback.format_stack()))
            if action==1:
                done=False
            #print(message)
            await self.game_recorder[agent.name].store_game_reward(info_index,message,new_reward,old_rewards,current_rewards)
            
            return self.basic_func[agent.name]["get_state"](agent),new_reward,done,current_reward
        return next_state_function

    async def end_bullet_time(self):#bullet_time is 0
        self.bullet_timer=0
        self.flag_dict["bullet_time"]=False
        await self.check_timer_change("timer_bullet",self.bullet_timer)
        self.initinal_turn_timer+=time.perf_counter()-self._elapsed_time

        for name_player in self.players_socket:
            socket:"WebSocket"=self.players_socket[name_player]
            #game_recorder:GameRecorder=self.game_recorder[name_player]
            if socket!=None:
                try:
                    await socket.send_text("end_bullet()")
                except Exception as e:
                    print(e)
                    pass
                
            #await game_recorder.store_game_message("end_bullet()")

        key="{}_bullet_time_flag"
        for un in self.players:#username
            self.flag_dict[key.format(un)]=False
        #print(self.stack)
        if self.stack and not self.flag_dict["bullet_time"]:
            stack_item=self.stack.pop()
            func,card=stack_item["prepared_function"],stack_item["card"]
            self.action_processor.start_record()
            #print(func,card,self.attacker)
            self.action_processor.start_record()
            self.action_processor.add_action(actions.Play_Cards(card,card.player))
            self.action_processor.end_record()
            result=await func()
            
            self.action_processor.end_record()
            if result=="defender" and isinstance(card,Creature) :

                await card.check_dead()
                await self.attacker.check_dead()

                #if not card.get_flag("die") and not self.attacker.get_flag("die"):#如果是有Menace 就记数，有两个defender才会让attacker_defenders变false 
                if not (card.get_flag("die") or self.attacker.get_flag("die") or card.get_flag("exile") or self.attacker.get_flag("exile"))  or self.attacker.get_flag("Menace"):
                    max_defender_number=1 if not self.attacker.get_flag("Menace") else 2
                    await self.start_attack(card)
                    self.add_counter_dict("defender_number",1)
                    if self.counter_dict["defender_number"]>=max_defender_number:
                        self.flag_dict["attacker_defenders"]=False
                        self.counter_dict["defender_number"]=0
                    
                    
            

        #self.stack 用pop()把每一个函数调用
        if not self.flag_dict["bullet_time"]:
            self.reset_bullet_timer()

            if self.get_flag("attacker_defenders"):#如果attacker_defenders还是True 那attacker 就去攻击敌方英雄
                
                await self.attacker.check_dead()
                
                if not ( self.attacker.get_flag("die") or  self.attacker.get_flag("exile")) or self.attacker.get_flag("Menace"):
                    await self.start_attack(self.non_active_player)
                self.flag_dict["attacker_defenders"]=False
                #print(self.flag_dict["attacker_defenders"])
            await self.check_death()
            #print(self.attacker)
            if self.attacker and\
                not self.attacker.get_flag("Vigilance") and\
                self.attacker.get_counter_from_dict("attack_counter")<=0:

                self.action_processor.start_record()
                self.attacker.tap()
                self.action_processor.end_record()
            self.attacker=None
            


async def run_parallel_room(config_path:str,config_path_list:list,info_communication:"Info_Communication",worker_id:int):
    
    room=Multi_Agent_Parallel_Specific_Room(
        config_path,
        config_path_list,
        info_communication,
        worker_id
    )
    
    await room.game_start()
    await room.action_process_system()

def worker_process(config_path:str, config_path_list:list, info_communication:"Info_Communication", worker_id:int):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    asyncio.run(
        run_parallel_room(
            config_path,
            config_path_list,
            info_communication,
            worker_id
        )
    )

if __name__=="__main__":

    print(Multi_Agent_Parallel_Specific_Room.get_cards_sample_by_name(None,"land",4,False))
