from game.train_agent import Agent_Train
from game.rlearning.trainingRoom.training_parallel_room import Multi_Agent_Parallel_Room
from game.rlearning.utils.stack_simulation import get_stack_reward

class Multi_Agent_Parallel_Variable_Deck_Room(Multi_Agent_Parallel_Room):
    def __init__(self,env_config,info_communication,worker_id,inference_communication=None):
        super().__init__(env_config,info_communication,worker_id,inference_communication)
        self.pending_transitions={}

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

    async def get_agent_state_action(self,agent,use_model=True):
        if not use_model:
            return None,None,1

        state=self.basic_func[agent.name]["get_state"](agent)
        mask=self.basic_func[agent.name]["create_action_mask"](agent)
        state["mask"]=mask

        if agent==self.player_1:
            await self.finish_pending_transition(agent,state)

        action=agent.choose_action(state,isTrain=True)
        return state,mask,action

    async def finish_pending_transition(self,agent,next_state,terminal=False):
        pending=self.pending_transitions.pop(agent.name,None)
        if pending is None:
            return

        state,action,reward_func=pending

        async def collect_transition():
            return await reward_func(next_state,terminal)

        await agent.store_data(state,action,collect_transition)

    async def execute_action(self,agent,action,reset_response=False):
        action=int(action)
        message=await self.basic_func[agent.name]["num2action"](agent,action)
        self.basic_func[agent.opponent.name]["add_opponent_history"](agent.opponent,agent,message)
        username,action_type,content=message.split("|",2)

        if reset_response and self.get_flag("bullet_time") and self.trigger_bullet_response(action_type):
            self.reset_bullet_pass()

        old_rewards=await get_stack_reward(self, agent)
        old_reward=old_rewards["reward"]
        info_index=len(self.game_recorder[agent.name].datas)
        result=await self.message_process_dict[action_type](username,content)
        await self.check_death()
        success=result is None or result[0]

        async def next_state_function(next_state,terminal=False):
            current_rewards=await get_stack_reward(self, agent)
            current_reward=current_rewards["reward"]
            gamma = agent.agent.config["ppo"]["gamma"]
            shaping_weight = 0.1

            done = terminal or await self.check_player_die()
            task_reward = 0.0

            if done:
                self_dead = await agent.check_dead()
                opponent_dead = await agent.opponent.check_dead()
                task_reward = float(opponent_dead) - float(self_dead)

            next_potential = 0.0 if done else current_reward

            shaping_reward = shaping_weight * (
                gamma * next_potential - old_reward
            )

            reward = task_reward + shaping_reward
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
            state,mask,action=await self.get_agent_state_action(current_agent,use_model)
            action_type,success,reward_func=await self.execute_action(current_agent,action,reset_response=True)

            if current_agent==self.player_1 and use_model:
                self.pending_transitions[current_agent.name]=(state,action,reward_func)

            if not success:
                first_response=False
                continue
            if not self.get_flag("bullet_time") or not self.gamming:
                return
            if action_type!="activate_ability":
                current_agent=current_agent.opponent

            first_response=False

        raise RuntimeError(f"bullet response exceeded max_bullet_actions={max_bullet_actions}")

    async def process_action(self,agent,action,state):
        action_type,success,reward_func=await self.execute_action(agent,action)

        if agent==self.player_1:
            self.pending_transitions[agent.name]=(state,action,reward_func)

        if success and self.trigger_bullet_response(action_type) and self.get_flag("bullet_time") and self.gamming:
            await self.run_bullet_response(agent,action_type)

        return reward_func

    async def action_process_system(self):
        while True:
            while self.gamming:
                agent=self.active_player
                state,mask,action=await self.get_agent_state_action(agent)
                await self.process_action(agent,action,state)
                await self.check_death()

            if self.player_1.name in self.pending_transitions:
                terminal_state=self.basic_func[self.player_1.name]["get_state"](self.player_1)
                await self.finish_pending_transition(self.player_1,terminal_state,terminal=True)

            self.send_data_to_host(self.player_1)
            self.pending_transitions.clear()
            self.gamming=True
            await self.initinal_environmrnt()