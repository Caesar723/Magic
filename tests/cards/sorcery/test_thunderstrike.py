from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestThunderstrike(CardTestCaseBase):
    async def test_thunderstrike_deals_heavy_damage_to_chosen_creature(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Thunderstrike/model.py", "Thunderstrike")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Thunder Target", 3, 3, 1)[0]
        life_before = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotEqual(env.card_zone(target), "battlefield")
        self.assertLess(env.p2.life, life_before)

    async def test_thunderstrike_survivor_does_not_splash_opponent_life(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Thunderstrike/model.py", "Thunderstrike")
        env = self.make_env()
        card = card_cls(env.p1)
        tank = env.put_creatures(env.p2, "Tank", 10, 12, 1)[0]
        life_before = env.p2.life

        def _pick_tank(seq):
            return tank if tank in seq else seq[0]

        with patch("game.game_function_tool.random.choice", side_effect=_pick_tank):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(tank), "battlefield")
        self.assertEqual(env.p2.life, life_before)
        self.assertEqual(tank.state[1], 4)

    async def test_thunderstrike_does_not_damage_controller_life(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Thunderstrike/model.py", "Thunderstrike")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Victim", 2, 2, 1)
        life_before = env.p1.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life_before)
