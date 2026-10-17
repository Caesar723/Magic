from game.train_agent import Agent_Train
from game.rlearning.trainingRoom.training_parallel_room import Multi_Agent_Parallel_Room


class Multi_Agent_Parallel_Variable_Deck_Room(Multi_Agent_Parallel_Room):
    def __init__(self,env_config,info_communication,worker_id,inference_communication=None):
        super().__init__(env_config,info_communication,worker_id,inference_communication)
        self.response_transitions=[]

    def initinal_player(self,players,is_initinal=True):
        super().initinal_player(players,is_initinal)
        self.player_1.config=self.player_1.agent.config
        self.player_2.config=self.player_2.agent.config

    @staticmethod
    def enable_bullet_response(agent):
        return isinstance(agent,Agent_Train) and agent.agent.config.get("enable_bullet_response",False)

    @staticmethod
    def trigger_bullet_response(action_type):
        return action_type in {"play_card","select_attacker","select_defender"}

    def reset_bullet_pass(self):
        for player_name in self.players:
            self.flag_dict[f"{player_name}_bullet_time_flag"]=False

    def get_agent_state_action(self,agent,use_model=True):
        if not use_model:
            return None,None,1
        state=self.basic_func[agent.name]["get_state"](agent)
        mask=self.basic_func[agent.name]["create_action_mask"](agent)
        state["mask"]=mask
        action=agent.choose_action(state,isTrain=True)
        return state,mask,action

    async def execute_action(self,agent,action,snapshot_next_state=False,reset_response=False):
        action=int(action)
        message=await self.basic_func[agent.name]["num2action"](agent,action)
        self.basic_func[agent.opponent.name]["add_opponent_history"](agent.opponent,agent,message)
        username,action_type,content=message.split("|",2)

        if reset_response and self.get_flag("bullet_time") and self.trigger_bullet_response(action_type):
            self.reset_bullet_pass()

        old_rewards=self.basic_func[agent.name]["get_reward"](agent)
        old_reward=old_rewards["reward"]
        info_index=len(self.game_recorder[agent.name].datas)
        attacker=self.attacker if action==1 or 12<=action<=21 else None
        selected_creature=agent.battlefield[int(content)] if 2<=action<=21 else None

        result=await self.message_process_dict[action_type](username,content)
        await self.check_death()
        success=result is None or result[0]
        saved_transition=None

        async def collect_transition():
            current_rewards=self.basic_func[agent.name]["get_reward"](agent,selected_creature,attacker)
            current_reward=current_rewards["reward"]
            reward=(current_reward-old_reward)/5

            if action==0:
                reward/=50
            if self.config.get("long_sight",False) and (2<=action<=11 or action==0):
                reward=0

            reward=max(min(reward,0.3),-0.3)
            died=await self.check_player_die()
            done=False

            if died and agent.life<=0:
                reward=-1
                done=True
            elif died:
                reward=1
                done=True
            if action==1 and not self.enable_bullet_response(agent):
                done=False

            next_state=self.basic_func[agent.name]["get_state"](agent)
            return next_state,reward,done,current_reward,current_rewards

        if success and snapshot_next_state:
            saved_transition=await collect_transition()

        async def next_state_function():
            transition=saved_transition if saved_transition is not None else await collect_transition()
            next_state,reward,done,current_reward,current_rewards=transition
            current_info_index=len(self.game_recorder[agent.name].datas) if action==0 else info_index
            await self.game_recorder[agent.name].store_game_reward(current_info_index,message,reward,old_rewards,current_rewards)
            return next_state,reward,done,current_reward

        return action_type,success,next_state_function

    async def run_bullet_response(self,trigger_agent,trigger_action_type):
        self.reset_bullet_pass()
        current_agent=trigger_agent.opponent
        first_response=True
        max_bullet_actions=trigger_agent.agent.config.get("max_bullet_actions",32)

        for _ in range(max_bullet_actions):
            if not self.get_flag("bullet_time") or not self.gamming:
                return

            force_model=first_response and trigger_action_type=="select_attacker"
            use_model=force_model or self.enable_bullet_response(current_agent)
            state,mask,action=self.get_agent_state_action(current_agent,use_model)
            snapshot_next_state=use_model and self.enable_bullet_response(current_agent)
            action_type,success,reward_func=await self.execute_action(current_agent,action,snapshot_next_state,reset_response=True)

            if not success:
                first_response=False
                continue
            if current_agent==self.player_1 and use_model:
                self.response_transitions.append((current_agent,state,action,reward_func))
            if not self.get_flag("bullet_time") or not self.gamming:
                return
            if action_type!="activate_ability":
                current_agent=current_agent.opponent

            first_response=False

        raise RuntimeError(f"bullet response exceeded max_bullet_actions={max_bullet_actions}")

    async def process_action(self,agent,action):
        if not self.enable_bullet_response(agent) and not self.enable_bullet_response(agent.opponent):
            return await super().process_action(agent,action)

        snapshot_next_state=self.enable_bullet_response(agent)
        action_type,success,reward_func=await self.execute_action(agent,action,snapshot_next_state)

        if success and self.trigger_bullet_response(action_type) and self.get_flag("bullet_time") and self.gamming:
            await self.run_bullet_response(agent,action_type)

        return reward_func

    async def store_response_transitions(self):
        for agent,state,action,reward_func in self.response_transitions:
            await agent.store_data(state,action,reward_func)
        self.response_transitions.clear()

    async def action_process_system(self):
        repeat_train=True

        while repeat_train:
            while self.gamming:
                self.response_transitions.clear()
                agent=self.active_player
                state=self.basic_func[agent.name]["get_state"](agent)
                mask=self.basic_func[agent.name]["create_action_mask"](agent)
                state["mask"]=mask
                action=agent.choose_action(state,isTrain=True)
                reward_func=await self.process_action(agent,action)
                oppo_agent=agent.opponent

                if agent==self.player_1:
                    if action!=0:
                        await agent.store_data(state,action,reward_func)
                    else:
                        async def store_data_func(agent=agent,state=state,action=action,reward_func=reward_func):
                            await agent.store_data(state,action,reward_func)
                        agent.add_pedding_store_task(store_data_func)

                await self.store_response_transitions()

                await self.check_death()

            if agent==self.player_1:
                self.send_data_to_host(agent)
            else:
                self.send_data_to_host(oppo_agent)

            self.gamming=True
            await self.initinal_environmrnt()
