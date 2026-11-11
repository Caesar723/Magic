from game.train_agent import Agent_Train
from game.game_recorder import GameRecorder
from game.rlearning.utils.model import get_class_by_name
from game.rlearning.trainingRoom.training_parallel_specific_orgpos_room import (
    Multi_Agent_Parallel_Specific_Orgpos_Room,
)


class ConditionEventPlayer(Agent_Train):
    def __init__(self, name, room, agent):
        self._draw_depth = 0
        super().__init__(name, room, agent)

    def _events(self):
        return getattr(self.room, "_condition_events", None)

    def draw_card(self, number):
        self._draw_depth += 1
        try:
            return super().draw_card(number)
        finally:
            self._draw_depth -= 1

    async def take_damage(self, card, value):
        before = self.life
        result = await super().take_damage(card, value)
        events = self._events()

        if events is not None:
            index = events["players"].index(self.name)
            events["player_damage"][index] += max(
                0,
                before - self.life,
            )
        return result

    async def gains_life(self, card, value):
        before = self.life
        result = await super().gains_life(card, value)
        events = self._events()

        if events is not None:
            index = events["players"].index(self.name)
            events["player_heal"][index] += max(
                0,
                self.life - before,
            )
        return result

    def remove_card(self, card, zone_name):
        events = self._events()
        zone = getattr(self, zone_name, ())
        existed = events is not None and card in zone
        card_id = int(card.card_id) if existed else None
        result = super().remove_card(card, zone_name)

        if existed and card not in zone:
            events["removed"][id(card)] = (zone_name, card_id)
        return result

    def append_card(self, card, zone_name):
        events = self._events()
        origin = events["removed"].pop(id(card), None) if events else None
        result = super().append_card(card, zone_name)

        if events is None or origin is None:
            return result

        source_zone, card_id = origin

        if source_zone == "battlefield" and zone_name == "graveyard":
            events["dead_ids"].add(card_id)

        if (
            source_zone == "library"
            and zone_name == "hand"
            and self._draw_depth > 0
        ):
            index = events["players"].index(self.name)
            events["draw_counts"][index] += 1

        return result

    async def store_data(self, state, action, reward_func):
        state = dict(state)

        async def collect_reward():
            next_state, reward, done, global_reward = await reward_func()
            next_state = dict(next_state)
            targets = next_state.pop(
                "_condition_event_targets",
                None,
            )

            if targets is not None:
                state["event_targets"] = targets

            return next_state, reward, done, global_reward

        return await super().store_data(
            state,
            action,
            collect_reward,
        )


class ConditionEventRoom(Multi_Agent_Parallel_Specific_Orgpos_Room):
    def __init__(
        self,
        env_config,
        info_communication,
        worker_id,
        inference_communication=None,
    ):
        self._condition_events = None
        self.inference_communication = inference_communication
        super().__init__(
            env_config,
            info_communication,
            worker_id,
        )

    def initinal_player(self, players=None, is_initinal=True):
        model_info = self.info_communication.get_model_info(
            self.worker_id
        )
        opponent_agent = self.agent_list[
            model_info["config_opponent_path"]
        ]

        self.player_1 = ConditionEventPlayer(
            "Agent1",
            self,
            self.agent1,
        )
        self.player_2 = ConditionEventPlayer(
            "Agent2",
            self,
            opponent_agent,
        )
        self.player_1.agent.pbar = None
        self.player_1.set_opponent_player(self.player_2, self)
        self.player_2.set_opponent_player(self.player_1, self)

        for player in (self.player_1, self.player_2):
            for treasure in player.agent.config.get("treasures", []):
                player.treasure.append(
                    get_class_by_name(treasure)()
                )
            player.change_function_by_treasure()

        self.players = {
            "Agent1": self.player_1,
            "Agent2": self.player_2,
        }
        self.players_socket = {
            "Agent1": None,
            "Agent2": None,
        }

        if is_initinal:
            self.update_flag = {
                "Agent1": False,
                "Agent2": False,
            }
            self.game_recorder = {
                "Agent1": GameRecorder(self.player_1, self),
                "Agent2": GameRecorder(self.player_2, self),
            }

        self.basic_func = {
            "Agent1": self.initinal_function(
                self.player_1.agent.config
            ),
            "Agent2": self.initinal_function(
                self.player_2.agent.config
            ),
        }

        self.player_1.agent.reset_rollout_context()
        self.player_2.agent.reset_rollout_context()

    async def process_action(self, agent, action):
        if action == 0 or self._condition_events is not None:
            return await super().process_action(agent, action)

        events = {
            "players": [agent.name, agent.opponent.name],
            "removed": {},
            "dead_ids": set(),
            "player_damage": [0, 0],
            "player_heal": [0, 0],
            "draw_counts": [0, 0],
        }
        self._condition_events = events

        try:
            reward_func = await super().process_action(agent, action)
        finally:
            self._condition_events = None

        async def collect_reward():
            previous = self._condition_events
            self._condition_events = events

            try:
                next_state, reward, done, global_reward = await reward_func()
            finally:
                self._condition_events = previous

            next_state = dict(next_state)
            next_state["_condition_event_targets"] = {
                "version": 1,
                "dead_ids": sorted(events["dead_ids"]),
                "player_damage": events["player_damage"],
                "player_heal": events["player_heal"],
                "draw_counts": events["draw_counts"],
            }
            return next_state, reward, done, global_reward

        return collect_reward