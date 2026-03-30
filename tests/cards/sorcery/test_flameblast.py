from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestFlameblast(CardTestCaseBase):
    async def test_flameblast_deals_five_to_target(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Flameblast/model.py", "Flameblast")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Flameblast Target", 2, 5, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotEqual(env.card_zone(target), "battlefield")

    async def test_flameblast_can_target_player_for_five(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Flameblast/model.py", "Flameblast")
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
        self.assertEqual(env.p2.life, life_before - 5)

    async def test_flameblast_controller_life_unchanged_when_burning_creature(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Flameblast/model.py", "Flameblast")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Flameblast Target", 2, 5, 1)
        ctrl_life = env.p1.life

        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, ctrl_life)
