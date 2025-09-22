
if __name__=="__main__":
    import sys
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/src")
    
   

#from room_server import RoomServer
import numpy as np
import asyncio

from game.agent import Agent_Player as Agent
from game.room import Room
from game.ppo_train import Agent_PPO
from game.rlearning.module.ppo_agent import PPOTrainer
from game.rlearning.utils.model import get_class_by_name

from game.card import Card
from game.type_cards.creature import Creature
from game.type_cards.instant import Instant
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery
from game.rlearning.utils.file import read_yaml








class Base_Agent_Room(Room):

    """
    0:end turn
    1:end bullet time
    2-11:选择一个随从进行攻击(10) 
    12-21:选择一个随从进行阻挡(10)

    22-351
    有10张手牌 对于每一张牌(10 * 33)
        player a card 不选择
        
        player a card 选择敌方随从0-9 总共10个随从
        player a card 选择我方随从0-9 总共10个随从

        player a card 选择敌方英雄
        player a card 选择我方英雄
        player a card 选择一个卡牌 (10)
    """

    def __init__(self,players:list[tuple],room_server) -> None:#((deck,user_name1),...)
        self.reward_dict:dict[str,function]={
            "reward_balance":self.get_reward_balance,
            "reward_attack":self.get_reward_attack,
            "reward_life":self.get_reward_life,
            "reward_win_base":self.get_reward_win_base,
            "reward_creature_base":self.get_reward_creature_base,
        }
        super().__init__(players,room_server)

        


    def num2action(self,agent:Agent,action:int)->str:
        if agent.agent.config.get("new_version",False):
            return self.num2action_new(agent,action)
        else:
            return self.num2action_old(agent,action)

    async def num2action_old(self,agent:Agent,action:int)->str:
        name=agent.name
        content=''
        if action==0:
            type_act="end_step"
        elif action==1:
            type_act="end_bullet"
        elif action>=2 and action<=11:
            type_act="select_attacker"
            content=f'{action-2}'
        elif action>=12 and action<=21:
            type_act="select_defender"
            content=f'{action-12}'
        else:
            type_act="play_card"
            index_card=(action-22)//33
            content=f"{index_card}"
            sub_action=(action-22)%33
            sub_content=self.num2subaction(agent,sub_action)
            agent.set_select_content(sub_content)
            #print(sub_content)
        result=f"{name}|{type_act}|{content}"
        return result

    """
    0:end turn
    1:end bullet time
    2-11:选择一个随从进行攻击(10) 
    12-21:选择一个随从进行阻挡(10)

    22-1341
    有10张手牌 对于每一张牌(40 * 33)
        player a card 不选择
        
        player a card 选择敌方随从0-9 总共10个随从
        player a card 选择我方随从0-9 总共10个随从

        player a card 选择敌方英雄
        player a card 选择我方英雄
        player a card 选择一个卡牌 (10)
    """
    async def num2action_new(self,agent:Agent,action:int)->str:
        name=agent.name
        content=''
        sort_function=self.create_sort_function(agent)
        if action==0:
            type_act="end_step"
        elif action==1:
            type_act="end_bullet"
        elif action>=2 and action<=11:
            type_act="select_attacker"
            self_battlefield=agent.battlefield
            
            self_battlefield_sorted=sorted(enumerate(self_battlefield), key=lambda x: sort_function(x[1]), reverse=True)
            
            selected_index=self_battlefield_sorted[action-2][0]
            content=f'{selected_index}'
        elif action>=12 and action<=21:
            type_act="select_defender"
            
            self_battlefield=agent.battlefield
            
            self_battlefield_sorted=sorted(enumerate(self_battlefield), key=lambda x: sort_function(x[1]), reverse=True)
            
            selected_index=self_battlefield_sorted[action-12][0]
            content=f'{selected_index}'
        else:
            type_act="play_card"
            # print(action)
            # print(agent.id_dict)
            index_card=((action-22)//33)+1
            #print(index_card)
            key = next((k for k, v in agent.id_dict.items() if v == index_card), None)
            # print(key)
            # print(agent.hand)
            
            index_card=next((i for i, card in enumerate(agent.hand) if (f"{card.name}+{card.type}")==key), None)
            #print(index_card)
            content=f"{index_card}"
            sub_action=(action-22)%33
            sub_content=self.num2subaction(agent,sub_action)
            #print(sub_content)
            agent.set_select_content(sub_content)
            #print(sub_content)
        result=f"{name}|{type_act}|{content}"
        return result

    def num2subaction(self,agent:Agent,sub_action:int):
        name=agent.name
        content=''
        father_class="field"
        type_act=""

        
        sort_function=self.create_sort_function(agent)
        if sub_action==0:
            pass
        elif sub_action>=1 and sub_action<=10:
            opponent_battlefield=agent.opponent.battlefield
            opponent_battlefield_sorted=sorted(enumerate(opponent_battlefield), key=lambda x: sort_function(x[1]), reverse=True)
            type_act="opponent_battlefield"
            selected_index=opponent_battlefield_sorted[sub_action-1][0]
            content=f"{selected_index}"
        elif sub_action>=11 and sub_action<=20:
            self_battlefield=agent.battlefield
            
            self_battlefield_sorted=sorted(enumerate(self_battlefield), key=lambda x: sort_function(x[1]), reverse=True)
            
            selected_index=self_battlefield_sorted[sub_action-11][0]
            
            type_act="self_battlefield"
            content=f"{selected_index}"
        elif sub_action==21:
            type_act="oppo"
        elif sub_action==22:
            type_act="self"
        else:
            father_class="cards"
            type_act=f"{sub_action-11}"
            content=""
        result=f"{name}|{father_class}|{type_act}|{content}"
        return result



    
    async def check_player_die(self):
        died_player=[]
        for name in self.players:
            if (await self.players[name].check_dead()):
                died_player.append(self.players[name])
        return bool(died_player)




    """
    让状态归一
    1-我方英雄的血量/20
    1-敌方英雄的血量/20
    蓝色，红色，绿色，白色，黑色法力值（通过计算地牌来得出）/10
    卡牌(10):[编号，法力值]使用嵌入式（10*20）
        # 定义嵌入层
        # card_embedding = tf.keras.layers.Embedding(input_dim=100, output_dim=14)  # 卡牌编号的嵌入层
        (0,0,0,0,0,0)
        # hand_cards_embedded = tf.concat([
        #     card_embedding(hand_cards[:, 0]),
        #     mana_embedding(hand_cards[:, 1])
        # ], axis=-1)
    我方场地(10):[攻击力，生命值]/10 , [1,0]是否可以攻击和防御
    敌方场地(10):[攻击力，生命值]/10 , [1,0]是否可以攻击和防御
    时间状态[0,1]:本回合，敌方攻击
    攻击的随从[攻击力，生命值]/10
    """

    def get_state(self,agent:Agent):
        oppo_agent=agent.opponent

        self_life=1-agent.life/agent.ini_life
        oppo_life=1-oppo_agent.life/oppo_agent.ini_life

        lifes=np.array([self_life,oppo_life])

        cost=self.get_cost_total(agent)
        colors=np.array([cost["U"],cost["R"],cost["G"],cost["W"],cost["B"]])

        cards_hand_costs=[]
        length_hand=len(agent.hand)
        for hand_i in range(10):
            if hand_i <length_hand:
                card=agent.hand[hand_i]
                cards_hand_costs.append(list(card.calculate_cost().values()))
            else:
                cards_hand_costs.append([0,0,0,0,0,0])
        cards_hand_costs=np.array(cards_hand_costs)
        cards_hand_costs=cards_hand_costs.flatten()/10

        self_battlefield=self.get_creature_state(agent.battlefield)
        oppo_battlefield=self.get_creature_state(oppo_agent.battlefield)

        time_state=self.get_time_state()

        attacker=self.get_attacker()

        cards_id=[]
        for id_i in range(10):
            if id_i <length_hand:
                card=agent.hand[id_i]
                cards_id.append(agent.id_dict[f"{card.name}+{card.type}"])
            else:
                cards_id.append(0)

        cards_id=np.array(cards_id)
        
        num_state=np.concatenate((lifes,colors,cards_hand_costs,self_battlefield,oppo_battlefield,time_state,attacker))

        return num_state,cards_id


    """
    我方英雄血量长度 20
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]#血量为 19
    敌方英雄血量长度 20
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]#血量为 19
    法力值
    绿长度为 20 【1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0】#0
    蓝长度为 20 【0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1】#20
    红长度为 20 【1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0】
    白长度为 20 【1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0】
    黑长度为 20 【1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0】

    手牌长度 10:
        对于每一张卡牌
        编号 id 用 nn.embedding 嵌入
        卡牌类型 4 用 nn.embedding 嵌入
        特殊类型 长度 20
        【战吼，亡语，reach，Trample，flying，haste，Flash，lifelink，summoning_sickness,padding】


        合起来 长度 120
        法力无长度 20:【0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0】
        法力绿长度 20:【0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0】
        法力蓝长度 20:【0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0】
        法力红长度 20:【0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0】
        法力白长度 20:【0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0】
        法力黑长度 20:【0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0】

        攻击和防御
        【atk_n, hp_n】
        【has_attack, has_defend】

        
    场地长度 10:
        每一个随从
        特殊类型 长度 20
        【战吼，亡语，reach，Trample，flying，haste，Flash，lifelink，summoning_sickness,padding】
        【atk_n, hp_n】
        [has_attack, has_defend]

    敌方场地长度 10:
        每一个随从
        特殊类型 长度 20
        【战吼，亡语，reach，Trample，flying，haste，Flash，lifelink，summoning_sickness,padding】
        【atk_n, hp_n】
        [has_attack, has_defend]

        
    进攻随从 embed
    攻击和防御
    【atk_n, hp_n】
    [has_attack, has_defend]
    战吼，亡语，reach，Trample，flying，haste，Flash，lifelink，summoning_sickness,padding】


    """
    def get_new_state(self,agent:Agent):
        state_batch={}

        basic_state=[]
        oppo_agent=agent.opponent

        self_life=max(0,min(20,int(agent.life)))
        self_life_one_hot=np.zeros(21)
        self_life_one_hot[self_life]=1
        state_batch["self_life"]=self_life_one_hot

        oppo_life=max(0,min(20,int(oppo_agent.life)))
        oppo_life_one_hot=np.zeros(21)
        oppo_life_one_hot[oppo_life]=1
        state_batch["oppo_life"]=oppo_life_one_hot
        max_mana=20

       

        self_mana=[]
        cost=self.get_cost_total(agent)
        for color in ["U","R","G","W","B"]:
            mana_cost=cost[color]
            mana_cost=max(0,min(max_mana,int(mana_cost)))
            # one_hot=np.zeros(max_mana)
            # one_hot[mana_cost]=1
            self_mana.append(mana_cost)
        

        state_batch["self_mana"]=self_mana
            
        state_batch["action_history"]=agent.get_action_history()

        card_ids=[]
        card_types=[]
        card_special_types=[]
        card_costs=[]
        card_atks=[]
        card_hps=[]
        card_has_attack=[]
        card_has_defend=[]
        card_mask=[]
        
        length_hand=len(agent.hand)
        for hand_i in range(10):
            if hand_i <length_hand:
                card=agent.hand[hand_i]

                card_ids.append(agent.id_dict[f"{card.name}+{card.type}"])

                card_type,card_special_type=self.get_card_special_types(card)

                card_types.append(card_type)
                card_special_types.append(card_special_type)

                card_manas=[]
                for mana in list(card.calculate_cost().values()):
                    mana=max(0,min(max_mana,int(mana)))
                    # mana_one_hot=np.zeros(max_mana)
                    # mana_one_hot[mana]=1
                    card_manas.append(mana)
                #card_manas=np.concatenate(card_manas, axis=0)
                #print(card.calculate_cost().values())
                card_costs.append(np.array(card_manas))

                if card_type==1:
                    attack,defend=card.state
                    card_atks.append(attack)
                    card_hps.append(defend)
                    card_has_attack.append(1)
                    card_has_defend.append(1)
                else:
                    card_atks.append(0)
                    card_hps.append(0)
                    card_has_attack.append(0)
                    card_has_defend.append(0)

                card_mask.append(1)
            else:
                card_ids.append(0)
                card_types.append(0)
                card_special_types.append(np.zeros(20))
                card_costs.append(np.zeros(6))
                card_atks.append(0)
                card_hps.append(0)
                card_has_attack.append(0)
                card_has_defend.append(0)
                card_mask.append(0)


        state_batch["card_hand"]={}
        state_batch["card_hand"]["card_ids"]=np.array(card_ids)
        state_batch["card_hand"]["card_types"]=np.array(card_types)
        state_batch["card_hand"]["card_special_types"]=np.array(card_special_types)
        state_batch["card_hand"]["card_costs"]=np.array(card_costs)
        state_batch["card_hand"]["card_atks"]=np.array(card_atks)
        state_batch["card_hand"]["card_hps"]=np.array(card_hps)
        state_batch["card_hand"]["card_has_attack"]=np.array(card_has_attack)
        state_batch["card_hand"]["card_has_defend"]=np.array(card_has_defend)
        state_batch["card_hand"]["card_mask"]=np.array(card_mask)

        state_batch["self_board"]=self.get_creature_state_new_batch(agent,agent.battlefield)
        state_batch["oppo_board"]=self.get_creature_state_new_batch(agent,oppo_agent.battlefield)

        
        if self.get_flag("attacker_defenders"):
            state_batch["attacker"]=self.get_creature_state_new(self.attacker)
            
        else:
            state_batch["attacker"]={}
            state_batch["attacker"]["card_special_types"]=[np.zeros(20)]
            state_batch["attacker"]["card_atks"]=[0]
            state_batch["attacker"]["card_hps"]=[0]
            state_batch["attacker"]["card_has_attack"]=[0]
            state_batch["attacker"]["card_has_defend"]=[0]

        return state_batch


    def get_card_special_types(self,card:Card):
        special_types=np.zeros(20)

        card_type=0

        if isinstance(card,Creature):
            card_type=1
            if not (Creature.when_enter_battlefield is card.when_enter_battlefield.__func__):
                special_types[0]=1
            if not (Creature.when_leave_battlefield is card.when_leave_battlefield.__func__):
                special_types[1]=1
        elif isinstance(card,Instant):
            card_type=2
            if not (Instant.card_ability is card.card_ability.__func__):
                special_types[0]=1
        elif isinstance(card,Land):
            card_type=3
            if not (Land.when_enter_battlefield is card.when_enter_battlefield.__func__):
                special_types[0]=1
            if not (Land.when_leave_battlefield is card.when_leave_battlefield.__func__):
                special_types[1]=1
        elif isinstance(card,Sorcery):
            card_type=4
            if not (Sorcery.card_ability is card.card_ability.__func__):
                special_types[0]=1
            
            
        for i,flag in enumerate(["reach","Trample","flying","haste","Flash","lifelink"]):
            if card.get_flag(flag):
                special_types[2+i]=1

        if not card.get_flag("tap") and not card.get_flag("summoning_sickness"):
            special_types[8]=1
        return card_type,special_types

    
    def get_creature_state_new(self,creature:Creature):
        
        result={}
        _,card_special_type=self.get_card_special_types(creature)
        attack,defend=list(creature.state)

        result["card_special_types"]=[card_special_type]
        result["card_atks"]=[attack]
        result["card_hps"]=[defend]
        result["card_has_attack"]=[1]
        result["card_has_defend"]=[1]
        return result
    
    def get_creature_state_new_batch(self,agent:Agent,creatures:list[Creature]):
        length=len(creatures)
        batch_result={}
        batch_result["card_special_types"]=[]
        batch_result["card_atks"]=[]
        batch_result["card_hps"]=[]
        batch_result["card_has_attack"]=[]
        batch_result["card_has_defend"]=[]
        batch_result["card_mask"]=[]


        sort_function=self.create_sort_function(agent)
        cards_sorted = sorted(creatures, key=sort_function, reverse=True)
        #print(cards_sorted)
        for i in range(10):
            if i < length:
                creature=cards_sorted[i]
                result=self.get_creature_state_new(creature)
                batch_result["card_special_types"]+=result["card_special_types"]
                batch_result["card_atks"]+=result["card_atks"]
                batch_result["card_hps"]+=result["card_hps"]
                batch_result["card_has_attack"]+=result["card_has_attack"]
                batch_result["card_has_defend"]+=result["card_has_defend"]
                batch_result["card_mask"]+=[1]
            else:
                batch_result["card_special_types"]+=[np.zeros(20)]
                batch_result["card_atks"]+=[0]
                batch_result["card_hps"]+=[0]
                batch_result["card_has_attack"]+=[0]
                batch_result["card_has_defend"]+=[0]
                batch_result["card_mask"]+=[0]
        return batch_result

    def get_creature_state(self,array:list[Creature]):
        length=len(array)
        result=[]
        for i in range(10):
            if i < length:
                activate=[0]
                if not array[i].get_flag("tap") and not array[i].get_flag("summoning_sickness"):
                    activate=[10]
                result.append(list(array[i].state)+activate)
            else:
                result.append([0,0,0])
        result=np.array(result)
        result=result.flatten()/10
        return result
    
    def get_time_state(self):
        return np.array([0,1] if self.get_flag("attacker_defenders") else [1,0])
    
    def get_attacker(self):
        if self.get_flag("attacker_defenders"):
            result=list(self.attacker.state)
        else:
            result=[0,0]
        result=np.array(result)/10
        return result


    def get_cost_total(self,agent:Agent):
        player_mana=dict(agent.mana)
        for land in agent.land_area:
            if not land.get_flag("tap"):
                mana=land.generate_mana()
                for key in mana:
                    player_mana[key]+=mana[key]
        return player_mana


        


    async def initinal_environmrnt(self):# 返回一个state和评分
        self.turn_timer:int=0
        self.max_turn_time:int=120

        #used to count the time when player use instant and in bullet_time
        self.bullet_timer:int=0
        self.max_bullet_time:int=10


        #used to store the each flag like whether is bullet_time
        self.flag_dict:dict={}

        #used to store each counter like number of turns
        self.counter_dict:dict={}

        self.stack:list[tuple]=[]
        self.attacker:Creature=None
        # for task in self.tasks:
        #     task.cancel()
        self.tasks=[]
        self.initinal_player(None,is_initinal=False)


        for recorder_key in self.game_recorder:
            recorder=self.game_recorder[recorder_key]
            player=self.players[recorder_key]
            await recorder.save_binary(base_path=player.agent.logdir,extra_info=str(player.agent.step))
            #print(recorder.save_flag)

        self.action_store_list=[]
        if self.update_flag[self.player_1.name]:
            self.update_flag[self.player_1.name]=False
            self.update_flag[self.player_2.name]=False
            for recorder_key in self.game_recorder:
                self.game_recorder[recorder_key].reset_save_flag(self.players[recorder_key])
        
        await self.game_start()

    def create_action_mask(self,agent:Agent):
        if agent.agent.config.get("new_version",False):
            return self.create_action_mask_new(agent)
        else:
            return self.create_action_mask_old(agent)

    def create_action_mask_old(self,agent:Agent):
        oppo_agent=agent.opponent
        mask=np.zeros((352))
        if self.get_flag('attacker_defenders'):
            mask[1]=True
            for i,creat in enumerate(agent.battlefield):
                if i>=10:break
                if not creat.get_flag("tap") and \
        (not self.attacker.get_flag("flying") or (creat.get_flag("flying") or creat.get_flag("reach"))):
                    mask[12+i]=True
            #if agent.battlefield: mask[12:len(agent.battlefield)+12]=True
        else:
            mask[0]=True
            for i,creat in enumerate(agent.battlefield):
                if i>=10:break
                if (not creat.get_flag("summoning_sickness") or creat.get_flag("haste")) and\
        not creat.get_flag("tap") and (creat.get_counter_from_dict("attack_counter")>0):
                    mask[2+i]=True
            #if agent.battlefield: mask[2:len(agent.battlefield)+2]=True
            if agent.hand:self.mask_hand(agent,oppo_agent,mask)
        
        return mask[np.newaxis, :]


    def create_action_mask_new(self,agent:Agent):
        oppo_agent=agent.opponent
        mask=np.zeros((1342))

        self_battlefield_sorted=sorted(agent.battlefield, key=self.create_sort_function(agent), reverse=True)
        if self.get_flag('attacker_defenders'):
            mask[1]=True
            for i,creat in enumerate(self_battlefield_sorted):
                if i>=10:break
                    
                if not creat.get_flag("tap") and \
        (not self.attacker.get_flag("flying") or (creat.get_flag("flying") or creat.get_flag("reach"))):
                    mask[12+i]=True
            #if agent.battlefield: mask[12:len(agent.battlefield)+12]=True
        else:
            mask[0]=True
            for i,creat in enumerate(self_battlefield_sorted):
                if i>=10:break
                if (not creat.get_flag("summoning_sickness") or creat.get_flag("haste")) and\
        not creat.get_flag("tap") and (creat.get_counter_from_dict("attack_counter")>0):
                    mask[2+i]=True
            #if agent.battlefield: mask[2:len(agent.battlefield)+2]=True
            #print(agent.hand)
            if agent.hand:self.mask_hand_new(agent,oppo_agent,mask)
        
        return mask[np.newaxis, :]

    def create_sort_function(self,agent:Agent):
        def sort_function(card:Creature):
            score=self.get_creature_reward(card)
            if agent.agent.config.get("sort_method","score")=="score_tap":
                if (not card.get_flag("summoning_sickness") or card.get_flag("haste")) and\
                not card.get_flag("tap") and (card.get_counter_from_dict("attack_counter")>0):
                    score+=100
            return score
        return sort_function


    def mask_hand(self,agent:Agent,oppo_agent:Agent,mask:np.ndarray):
        start_index=22
        instance_dict={
            Creature:"when_enter_battlefield",
            Instant:"card_ability",
            Land:"when_enter_battlefield",
            Sorcery:"card_ability"
        }

        select_dict={
            'all_roles':[oppo_agent.battlefield,agent.battlefield,[1],[1]],
            'opponent_roles':[oppo_agent.battlefield,[],[],[1]], 
            'your_roles':[[],agent.battlefield,[1],[]],
            'all_creatures':[oppo_agent.battlefield,agent.battlefield,[],[]],
            'opponent_creatures':[oppo_agent.battlefield,[],[],[]],
            'your_creatures':[[],agent.battlefield,[],[]]
        }

        index_range=[10,10,1,1]
        #getattr(obj, 'my_attribute')
        card_counter=0
        for hand_card in agent.hand:
            if card_counter>=9:
                break
            if hand_card.check_can_use(agent)[0]:
                select_range=''
                for cls in instance_dict:
                    if isinstance(hand_card,cls):
                        select_range=getattr(hand_card,instance_dict[cls]).select_range
                #print(select_range)
                if select_range in select_dict:
                    self.select_stage(select_dict[select_range],index_range,start_index+1,mask)#+1 是因为有player a card 不选择
                elif hand_card.select_range in select_dict:
                    self.select_stage(select_dict[hand_card.select_range],index_range,start_index+1,mask)
                else:
                    mask[start_index]=True
            start_index+=33
            card_counter+=1



    def select_stage(self,selects,index_range,start_index,mask):
        index=start_index
        for select_list,ind_range in zip(selects,index_range):
            length=min(len(select_list),10)
            mask[index:length+index]=True
            # for i in range(len(select_list)):
            #     mask[index+i]=True
            index+=ind_range

    def mask_hand_new(self,agent:Agent,oppo_agent:Agent,mask:np.ndarray):
        start_index=22
        instance_dict={
            Creature:"when_enter_battlefield",
            Instant:"card_ability",
            Land:"when_enter_battlefield",
            Sorcery:"card_ability"
        }

        select_dict={
            'all_roles':[oppo_agent.battlefield,agent.battlefield,[1],[1]],
            'opponent_roles':[oppo_agent.battlefield,[],[],[1]], 
            'your_roles':[[],agent.battlefield,[1],[]],
            'all_creatures':[oppo_agent.battlefield,agent.battlefield,[],[]],
            'opponent_creatures':[oppo_agent.battlefield,[],[],[]],
            'your_creatures':[[],agent.battlefield,[],[]]
        }

        index_range=[10,10,1,1]
        #getattr(obj, 'my_attribute')
        card_counter=0
        for hand_card in agent.hand:
            if card_counter>=9:
                break
            current_index=start_index+(agent.id_dict[f"{hand_card.name}+{hand_card.type}"]-1)*33
            if hand_card.check_can_use(agent)[0]:
                select_range=''
                for cls in instance_dict:
                    if isinstance(hand_card,cls):
                        select_range=getattr(hand_card,instance_dict[cls]).select_range
                #print(select_range)
                if select_range in select_dict:
                    self.select_stage(select_dict[select_range],index_range,current_index+1,mask)#+1 是因为有player a card 不选择
                elif hand_card.select_range in select_dict:
                    self.select_stage(select_dict[hand_card.select_range],index_range,current_index+1,mask)
                else:
                    mask[current_index]=True
            #start_index+=33
            card_counter+=1

    def get_reward_balance(self,agent:Agent,battled_creature:Creature=None,attacker:Creature=None):#返回一个评分
        # if agent.life<=0:
        #     return -1
        # elif agent.opponent.life<=0:
        #     return 1
        self_live_reward=lambda x :x/5#lambda x :1/(1+np.e**(4-x))#用于红色的公式，卖血
        oppo_live_reward=lambda x :x/5

        score_life_self=self_live_reward(agent.life)
        score_oppo_self=oppo_live_reward(agent.opponent.life)

        score_battle_self_creatures=[self.get_creature_reward(card,battled_creature==card) for card in agent.battlefield]
        score_battle_self=sum(score_battle_self_creatures)#这个处以20表面随从不是很重要，重要的是敌方的血量
        
        score_battle_oppo_creatures=[self.get_creature_reward(card,card==attacker) for card in agent.opponent.battlefield]
        score_battle_oppo=sum(score_battle_oppo_creatures)

        score_mana=0
        for land in agent.land_area:
            score_mana+=sum(land.generate_mana().values())
        score_mana=score_mana/20
        score_hand=len(agent.hand)/30


        reward=score_hand+(score_life_self-score_oppo_self)+score_mana+score_battle_self-score_battle_oppo
        result={
            "reward":reward,
            "score_life_self":score_life_self,
            "score_oppo_self":score_oppo_self,
            "score_mana":score_mana,
            "score_hand":score_hand,
            "score_battle_self":score_battle_self,
            "score_battle_oppo":score_battle_oppo,
            "score_battle_self_creatures":score_battle_self_creatures,
            "score_battle_oppo_creatures":score_battle_oppo_creatures
        }
        #print(score_life_self,score_oppo_self,score_mana,score_battle_self,score_battle_oppo)

        return result

    def get_reward_attack(self,agent:Agent,battled_creature:Creature=None,attacker:Creature=None):#返回一个评分
        # if agent.life<=0:
        #     return -1
        # elif agent.opponent.life<=0:
        #     return 1
        self_live_reward=lambda x :x/20#lambda x :1/(1+np.e**(4-x))#用于红色的公式，卖血
        oppo_live_reward=lambda x :x/5

        score_life_self=self_live_reward(agent.life)
        score_oppo_self=oppo_live_reward(agent.opponent.life)

        score_battle_self_creatures=[self.get_creature_reward(card,battled_creature==card) for card in agent.battlefield]
        score_battle_self=sum(score_battle_self_creatures)#这个处以20表面随从不是很重要，重要的是敌方的血量
        
        score_battle_oppo_creatures=[self.get_creature_reward(card,card==attacker) for card in agent.opponent.battlefield]
        score_battle_oppo=sum(score_battle_oppo_creatures)

        score_mana=0
        for land in agent.land_area:
            score_mana+=sum(land.generate_mana().values())
        score_mana=score_mana/20
        score_hand=len(agent.hand)/30


        reward=score_hand+(score_life_self-score_oppo_self)+score_mana+score_battle_self-score_battle_oppo
        result={
            "reward":reward,
            "score_life_self":score_life_self,
            "score_oppo_self":score_oppo_self,
            "score_mana":score_mana,
            "score_hand":score_hand,
            "score_battle_self":score_battle_self,
            "score_battle_oppo":score_battle_oppo,
            "score_battle_self_creatures":score_battle_self_creatures,
            "score_battle_oppo_creatures":score_battle_oppo_creatures
        }
        #print(score_life_self,score_oppo_self,score_mana,score_battle_self,score_battle_oppo)

        return result

    def get_reward_life(self,agent:Agent,battled_creature:Creature=None,attacker:Creature=None):#返回一个评分
        # if agent.life<=0:
        #     return -1
        # elif agent.opponent.life<=0:
        #     return 1
        self_live_reward=lambda x :x/5#lambda x :1/(1+np.e**(4-x))#用于红色的公式，卖血
        oppo_live_reward=lambda x :x/10

        score_life_self=self_live_reward(agent.life)
        score_oppo_self=oppo_live_reward(agent.opponent.life)

        score_battle_self_creatures=[self.get_creature_reward(card,battled_creature==card) for card in agent.battlefield]
        score_battle_self=sum(score_battle_self_creatures)
        score_battle_oppo_creatures=[self.get_creature_reward(card,card==attacker) for card in agent.opponent.battlefield]
        score_battle_oppo=sum(score_battle_oppo_creatures)

        # score_battle_self=sum(
        #     [
        #         self.get_creature_reward(card,battled_creature==card) for card in agent.battlefield
        #     ]
        # )#这个处以20表面随从不是很重要，重要的是敌方的血量
        
        # score_battle_oppo=sum(
        #     [
        #         self.get_creature_reward(card) for card in agent.opponent.battlefield
        #     ]
        # )

        score_mana=0
        for land in agent.land_area:
            score_mana+=sum(land.generate_mana().values())

        score_hand=len(agent.hand)/30
        score_mana=score_mana/20

        reward=score_hand+(score_life_self-score_oppo_self)+score_mana+score_battle_self-score_battle_oppo

        result={
            "reward":reward,
            "score_life_self":score_life_self,
            "score_oppo_self":score_oppo_self,
            "score_mana":score_mana,
            "score_hand":score_hand,
            "score_battle_self":score_battle_self,
            "score_battle_oppo":score_battle_oppo,
            "score_battle_self_creatures":score_battle_self_creatures,
            "score_battle_oppo_creatures":score_battle_oppo_creatures
        }
        #print(score_life_self,score_oppo_self,score_mana,score_battle_self,score_battle_oppo)

        return result

    def get_reward_win_base(self,agent:Agent,battled_creature:Creature=None,attacker:Creature=None):#返回一个评分
        # if agent.life<=0:
        #     return -1
        # elif agent.opponent.life<=0:
        #     return 1
        self_live_reward=lambda x :x/5#lambda x :1/(1+np.e**(4-x))#用于红色的公式，卖血
        oppo_live_reward=lambda x :x/5

        score_life_self=self_live_reward(agent.life)
        score_oppo_self=oppo_live_reward(agent.opponent.life)

        score_battle_self_creatures=[self.get_creature_reward(card,battled_creature==card) for card in agent.battlefield]
        score_battle_self=sum(score_battle_self_creatures)
        
        
        score_battle_oppo_creatures=[self.get_creature_reward(card,card==attacker) for card in agent.opponent.battlefield]
        score_battle_oppo=sum(score_battle_oppo_creatures)

        # score_battle_self=sum(
        #     [
        #         self.get_creature_reward(card,battled_creature==card) for card in agent.battlefield
        #     ]
        # )#这个处以20表面随从不是很重要，重要的是敌方的血量
        
        # score_battle_oppo=sum(
        #     [
        #         self.get_creature_reward(card) for card in agent.opponent.battlefield
        #     ]
        # )

        score_mana=0
        for land in agent.land_area:
            score_mana+=sum(land.generate_mana().values())

        score_hand=len(agent.hand)/30
        score_mana=score_mana/20

        reward=score_hand+(score_life_self-score_oppo_self)+score_mana+score_battle_self-score_battle_oppo

        strength=3
        #print(agent.get_counter_from_dict("turn_count"))
        reward=reward/((agent.get_counter_from_dict("turn_count")+strength)/strength)
        result={
            "reward":reward,
            "score_life_self":score_life_self,
            "score_oppo_self":score_oppo_self,
            "score_mana":score_mana,
            "score_hand":score_hand,
            "score_battle_self":score_battle_self,
            "score_battle_oppo":score_battle_oppo,
            "score_battle_self_creatures":score_battle_self_creatures,
            "score_battle_oppo_creatures":score_battle_oppo_creatures
        }
        #print(score_life_self,score_oppo_self,score_mana,score_battle_self,score_battle_oppo)

        return result

    def get_reward_creature_base(self,agent:Agent,battled_creature:Creature=None,attacker:Creature=None):#返回一个评分
        # if agent.life<=0:
        #     return -1
        # elif agent.opponent.life<=0:
        #     return 1
        self_live_reward=lambda x :x/5#lambda x :1/(1+np.e**(4-x))#用于红色的公式，卖血
        oppo_live_reward=lambda x :x/5

        score_life_self=self_live_reward(agent.life)
        score_oppo_self=oppo_live_reward(agent.opponent.life)

        score_battle_self_creatures=[self.get_creature_reward(card,battled_creature==card) for card in agent.battlefield]
        score_battle_self=sum(score_battle_self_creatures)
        
        
        score_battle_oppo_creatures=[self.get_creature_reward(card,card==attacker) for card in agent.opponent.battlefield]
        score_battle_oppo=sum(score_battle_oppo_creatures)

        # score_battle_self=sum(
        #     [
        #         self.get_creature_reward(card,battled_creature==card) for card in agent.battlefield
        #     ]
        # )#这个处以20表面随从不是很重要，重要的是敌方的血量
        
        # score_battle_oppo=sum(
        #     [
        #         self.get_creature_reward(card) for card in agent.opponent.battlefield
        #     ]
        # )

        score_mana=0
        for land in agent.land_area:
            score_mana+=sum(land.generate_mana().values())

        score_hand=len(agent.hand)/30
        score_mana=score_mana/20

        reward=score_hand+(score_life_self-score_oppo_self)+score_mana+score_battle_self-score_battle_oppo

        strength=8
        #print(agent.get_counter_from_dict("turn_count"))
        reward=reward/((agent.get_counter_from_dict("turn_count")+strength)/strength)
        result={
            "reward":reward,
            "score_life_self":score_life_self,
            "score_oppo_self":score_oppo_self,
            "score_mana":score_mana,
            "score_hand":score_hand,
            "score_battle_self":score_battle_self,
            "score_battle_oppo":score_battle_oppo,
            "score_battle_self_creatures":score_battle_self_creatures,
            "score_battle_oppo_creatures":score_battle_oppo_creatures
        }
        #print(score_life_self,score_oppo_self,score_mana,score_battle_self,score_battle_oppo)

        return result

        # return score_hand+(score_life_self-score_oppo_self)+score_mana+score_battle_self-score_battle_oppo

    def get_creature_reward(self,card:Creature,in_battle:bool=False):
        if (card.get_flag("tap") or card.get_flag("summoning_sickness")) and not in_battle:
            p,d=card.power,card.live

            if p<=0 or d<=0:
                return 0
            state1=(p+d)/2
            state2=(p*d)**0.5
            r_state=(state1+state2)/12
            return r_state+0.05
        p,d=card.state[0],card.state[1]
        if p<=0 or d<=0:
            return 0
        state1=(p+d)/2
        state2=(p*d)**0.5
        r_state=(state1+state2)/10
        for flag in ["reach","Trample","flying","haste","Flash","lifelink"]:
            if card.get_flag(flag):
                r_state*=1.1
        return r_state+0.05
