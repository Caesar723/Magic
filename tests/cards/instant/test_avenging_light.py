from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestAvenging_Light(CardTestCaseBase):
    async def test_avenging_light_exiles_creature_and_gains_life_equal_power(self):
        card_cls = load_card_class_from_path("pycards/Instant/Avenging_Light/model.py", "Avenging_Light")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Avenging Target", 4, 4, 1)[0]
        env.p1.life = 10
        life_before = env.p1.life
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "exile_area")
        self.assertEqual(env.p1.life, life_before + 4)

    async def test_avenging_light_zero_power_creature_no_life_gain(self):
        card_cls = load_card_class_from_path("pycards/Instant/Avenging_Light/model.py", "Avenging_Light")
        env = self.make_env()
        card = card_cls(env.p1)
        target = env.put_creatures(env.p2, "Zero P", 0, 3, 1)[0]
        env.p1.life = 15
        life_before = env.p1.life
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "exile_area")
        self.assertEqual(env.p1.life, life_before)

    async def test_avenging_light_opponent_life_unchanged_when_exiling_creature(self):
        card_cls = load_card_class_from_path("pycards/Instant/Avenging_Light/model.py", "Avenging_Light")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Avenging Target", 3, 3, 1)
        env.p1.life = 10
        opp_before = env.p2.life

        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_before)
