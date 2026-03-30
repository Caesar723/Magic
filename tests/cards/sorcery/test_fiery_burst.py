from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestFiery_Burst(CardTestCaseBase):
    async def test_fiery_burst_deals_two_damage(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Fiery_Burst/model.py", "Fiery_Burst")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Burst Target", 2, 2, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotEqual(env.card_zone(target), "battlefield")

    async def test_fiery_burst_can_hit_player_for_two(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Fiery_Burst/model.py", "Fiery_Burst")
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
        self.assertEqual(env.p2.life, life_before - 2)

    async def test_fiery_burst_controller_life_unchanged_when_burning_creature(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Fiery_Burst/model.py", "Fiery_Burst")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Burst Target", 2, 2, 1)
        ctrl_life = env.p1.life

        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, ctrl_life)
