from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestBlaze_of_Fury(CardTestCaseBase):
    async def test_blaze_of_fury_deals_three_and_sets_cant_block(self):
        card_cls = load_card_class_from_path("pycards/Instant/Blaze_of_Fury/model.py", "Blaze_of_Fury")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Blaze Target", 2, 4, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(target.state[1], 1)
        self.assertTrue(target.get_flag("cant_block"))
        self.assertEqual(env.p1.life, 20)

    async def test_blaze_of_fury_can_damage_player(self):
        card_cls = load_card_class_from_path("pycards/Instant/Blaze_of_Fury/model.py", "Blaze_of_Fury")
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

    async def test_blaze_of_fury_controller_life_unchanged_when_creature_is_burned(self):
        card_cls = load_card_class_from_path("pycards/Instant/Blaze_of_Fury/model.py", "Blaze_of_Fury")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Solo", 2, 4, 1)
        life_before = env.p1.life
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life_before)
