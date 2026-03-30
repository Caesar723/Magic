from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestTorrential_Manipulation(CardTestCaseBase):
    async def test_torrential_manipulation_bounces_opponent_creature_as_new_instance(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Torrential_Manipulation/model.py", "Torrential_Manipulation")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Tide Target", 2, 2, 1)[0]
        hand_before = len(env.p2.hand)
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.hand), hand_before + 1)
        self.assertIsNot(env.p2.hand[-1], target)

    async def test_torrential_manipulation_random_opponent_player_target_is_noop(self):
        """
        `select_object("opponent_roles", …)` can yield the opponent `Player` as well as their
        battlefield. `card_ability` only returns a permanent from `opponent.battlefield` to hand;
        a Player selection is a no-op (no unreachable land-area path).
        """
        card_cls = load_card_class_from_path("pycards/sorcery/Torrential_Manipulation/model.py", "Torrential_Manipulation")
        env = self.make_env()
        card = card_cls(env.p1)
        creature = env.put_creatures(env.p2, "On Board", 2, 2, 1)[0]
        hand_before = len(env.p2.hand)

        def _pick_player(seq):
            return env.p2 if env.p2 in seq else seq[0]

        with patch("game.game_function_tool.random.choice", side_effect=_pick_player):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(creature), "battlefield")
        self.assertEqual(len(env.p2.hand), hand_before)

    async def test_torrential_manipulation_empty_battlefield_player_only_noop(self):
        """With no opponent permanents on battlefield, the pool is only the opponent player."""
        card_cls = load_card_class_from_path("pycards/sorcery/Torrential_Manipulation/model.py", "Torrential_Manipulation")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p2.battlefield.clear()
        hand_before = len(env.p2.hand)
        life_before = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.hand), hand_before)
        self.assertEqual(env.p2.life, life_before)
