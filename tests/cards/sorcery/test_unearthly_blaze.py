from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestUnearthly_Blaze(CardTestCaseBase):
    async def test_unearthly_blaze_deals_three_to_any_target(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Unearthly_Blaze/model.py", "Unearthly_Blaze")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Blaze Target", 2, 3, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotEqual(env.card_zone(target), "battlefield")
        self.assertEqual(env.p1.life, 20)

    async def test_unearthly_blaze_can_hit_opponent_player_for_three(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Unearthly_Blaze/model.py", "Unearthly_Blaze")
        env = self.make_env()
        card = card_cls(env.p1)
        life_before = env.p2.life
        with patch(
            "game.game_function_tool.random.choice",
            side_effect=lambda seq: env.p2 if env.p2 in seq else seq[0],
        ):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, life_before - 3)

    async def test_unearthly_blaze_creature_on_board_untouched_when_burning_player(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Unearthly_Blaze/model.py", "Unearthly_Blaze")
        env = self.make_env()
        card = card_cls(env.p1)
        blocker = env.put_creatures(env.p2, "Blocker", 4, 4, 1)[0]

        with patch(
            "game.game_function_tool.random.choice",
            side_effect=lambda seq: env.p2 if env.p2 in seq else seq[0],
        ):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(blocker), "battlefield")
        self.assertEqual(blocker.state, (4, 4))
