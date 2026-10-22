import asyncio
import random
import traceback

import numpy as np

from game.rlearning.trainingRoom.training_parallel_variable_deck_room import Multi_Agent_Parallel_Variable_Deck_Room



class MatchLimit(Exception):
    pass


class Multi_Agent_Parallel_Evaluation_Room(Multi_Agent_Parallel_Variable_Deck_Room):
    def __init__(
        self,
        env_config,
        info_communication,
        worker_id,
        inference_communication=None,
    ):
        
        self.task_info = None

        super().__init__(
            env_config,
            info_communication,
            worker_id,
            inference_communication,
        )

        self.gamming = False

    def initinal_player(self, players, is_initinal=True):
        if self.task_info is not None:
            self.agent1.config = dict(self.agent1.config)
            self.agent1.config["decks"] = [self.task_info["agent_deck"]]

            opponent = self.agent_list[self.task_info["opponent_config"]]

            opponent.config = dict(opponent.config)
            opponent.config["decks"] = [self.task_info["opponent_deck"]]

        super().initinal_player(players, is_initinal)

    async def game_start(self):

        pass

    async def message_process(self):
        pass

    async def action_sender(self):
        pass

    async def initinal_environmrnt(self):
        task = self.task_info

        self.gamming = False
        self.flag_dict.clear()
        self.counter_dict.clear()
        self.stack.clear()
        self.attacker = None

        self.pending_transitions.clear()
        self.action_store_list.clear()
        self.action_store_list_cache.clear()
        self.message_process_queue.clear()

        self.action_processor.action_list.clear()
        self.action_processor.start_counter = -1

        self.turn_timer = 0
        self.bullet_timer = 0

        random.seed(task["game_seed"])
        np.random.seed(task["game_seed"])

        self.info_communication.set_current_task(task)

        self.initinal_player(None, is_initinal=True)

        for player, seed in (
            (self.player_1, task["agent_shuffle_seed"]),
            (self.player_2, task["opponent_shuffle_seed"]),
        ):
            deck = sorted(
                player.deck,
                key=lambda card: (
                    type(card).__module__,
                    type(card).__qualname__,
                ),
            )

            random.Random(seed).shuffle(deck)

            player.deck = deck
            player.hand = deck[:7]
            player.library = deck[7:]

            self.game_recorder[player.name].save_flag = True

        self.action_processor.set_game_recorder(None)

        self.opening = {
            player.name: [
                f"{type(card).__module__}.{type(card).__qualname__}"
                for card in player.deck
            ]
            for player in (self.player_1, self.player_2)
        }

        random.seed(task["game_seed"])
        np.random.seed(task["game_seed"])

        self.action_count = 0
        self.outcome = None

    async def get_agent_state_action(self, agent, use_model=True):
        if not use_model:
            return None, None, 1

        state = self.basic_func[agent.name]["get_state"](agent)
        mask = self.basic_func[agent.name]["create_action_mask"](agent)

        state["mask"] = mask

        action = agent.choose_action(
            state,
            isTrain=False,
        )

        return state, mask, action

    async def execute_action(self, agent, action, reset_response=False):
        limit = self.env_config["evaluation"]["max_actions"]

        if self.action_count >= limit:
            raise MatchLimit()

        self.action_count += 1
        action = int(action)

        message = await self.basic_func[agent.name]["num2action"](
            agent,
            action,
        )

        self.basic_func[agent.opponent.name]["add_opponent_history"](
            agent.opponent,
            agent,
            message,
        )

        username, action_type, content = message.split("|", 2)

        if (
            reset_response
            and self.get_flag("bullet_time")
            and self.trigger_bullet_response(action_type)
        ):
            self.reset_bullet_pass()

        result = await self.message_process_dict[action_type](
            username,
            content,
        )

        await self.check_death()

        if result is not None and not result[0]:
            raise RuntimeError(
                f"Game rejected action: {message}, reason: {result}"
            )

        self.action_store_list_cache.clear()
        await asyncio.sleep(0)

        return action_type, True, None

    async def process_action(self, agent, action, state):
        action_type, success, _ = await self.execute_action(
            agent,
            action,
        )

        if (
            success
            and self.trigger_bullet_response(action_type)
            and self.get_flag("bullet_time")
            and self.gamming
        ):
            await self.run_bullet_response(agent, action_type)

    async def run_bullet_response(self, trigger_agent, trigger_action_type):
        self.reset_bullet_pass()

        current_agent = trigger_agent.opponent
        first_response = True

        limit = trigger_agent.agent.config.get("max_bullet_actions", 32)

        for _ in range(limit):
            if not self.get_flag("bullet_time") or not self.gamming:
                return

            force_model = first_response and trigger_action_type == "select_attacker"

            use_model = force_model or self.enable_bullet_response(current_agent)

            _, _, action = await self.get_agent_state_action(current_agent, use_model)

            action_type, _, _ = await self.execute_action(current_agent, action, reset_response=True)

            if not self.get_flag("bullet_time") or not self.gamming:
                return

            if action_type != "activate_ability":
                current_agent = current_agent.opponent

            first_response = False

        raise RuntimeError("Response window exceeds max_bullet_actions")

    async def game_end(self, died_player):
        if self.outcome is not None:
            return

        dead = {player.name for player in died_player}

        if dead == {"Agent1", "Agent2"}:
            self.outcome = "draw"
        elif dead == {"Agent1"}:
            self.outcome = "loss"
        elif dead == {"Agent2"}:
            self.outcome = "win"
        else:
            raise RuntimeError(f"Unknown end game information: {dead}")

        self.gamming = False

    async def run_task(self):
        status = "completed"
        reason = "terminal"
        error = None

        self.action_count = 0
        self.outcome = None
        self.opening = None

        try:
            await self.initinal_environmrnt()

            self.active_player = self.players[
                self.task_info["first_player"]
            ]
            self.non_active_player = self.active_player.opponent

            self.gamming = True

            self.reset_turn_timer()

            await self.active_player.game_start()
            await self.non_active_player.game_start()
            await self.check_death()

            while self.gamming:
                agent = self.active_player

                state, _, action = await self.get_agent_state_action(
                    agent
                )

                await self.process_action(agent, action, state)
                await self.check_death()

            if self.outcome is None:
                raise RuntimeError("The game ended but there is no win or loss result")

        except MatchLimit:
            status = "truncated"
            reason = "max_actions"

        except Exception:
            status = "error"
            reason = "exception"
            error = traceback.format_exc()

        finally:
            self.gamming = False

            for player in self.players.values():
                await player.cancel_future_function()

        self.info_communication.store_game_data({
            **self.task_info,
            "worker_id": self.worker_id,
            "status": status,
            "outcome": (
                self.outcome if status == "completed" else None
            ),
            "reason": reason,
            "actions": self.action_count,
            "opening_cards": self.opening,
            "error": error,
        })

    async def action_process_system(self):
        self.info_communication.ready_queue.put(
            self.worker_id
        )

        while True:
            task = self.info_communication.get_task()

            if task is None:
                return

            self.task_info = task
            await self.run_task()