from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestLuminous_Guardian(CardTestCaseBase):
    async def test_luminous_guardian_etb_exiles_big_creature(self):
        card_cls = load_card_class_from_path("pycards/creature/Luminous_Guardian/model.py", "Luminous_Guardian")
        env = self.make_env()
        card = card_cls(env.p1)

        big_enemy = env.put_creatures(env.p2, "Big Enemy", 4, 4, 1)[0]
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        guardian = env.get_battlefield_creature(env.p1, "Luminous Guardian")
        self.assert_state(guardian, {"flags": {"flying": True, "lifelink": True}})
        self.assertNotIn(big_enemy, env.p2.battlefield)
        self.assertEqual(len(env.p2.exile_area), 1)

    async def test_luminous_guardian_does_not_exile_low_power_creature(self):
        card_cls = load_card_class_from_path("pycards/creature/Luminous_Guardian/model.py", "Luminous_Guardian")
        env = self.make_env()
        card = card_cls(env.p1)

        small = env.put_creatures(env.p2, "Small Enemy", 2, 2, 1)[0]

        with patch("game.game_function_tool.random.choice", side_effect=lambda s: small):
            result = await env.play_card(card, env.p1)
            await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertIn(small, env.p2.battlefield)
        self.assertEqual(len(env.p2.exile_area), 0)

    async def test_luminous_guardian_leave_returns_exiled_card(self):
        card_cls = load_card_class_from_path("pycards/creature/Luminous_Guardian/model.py", "Luminous_Guardian")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_creatures(env.p2, "Big Enemy", 4, 4, 1)
        env.script_selection(env.p1, [0])
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        guardian = env.get_battlefield_creature(env.p1, "Luminous Guardian")
        await env.move_to_graveyard(guardian)
        self.assertTrue(any(c.name == "Big Enemy" for c in env.p2.battlefield))

    async def test_luminous_guardian_exiles_exactly_three_power_creature(self):
        card_cls = load_card_class_from_path("pycards/creature/Luminous_Guardian/model.py", "Luminous_Guardian")
        env = self.make_env()
        card = card_cls(env.p1)
        boundary = env.put_creatures(env.p2, "Exactly Three", 3, 3, 1)[0]
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotIn(boundary, env.p2.battlefield)
        self.assertEqual(len(env.p2.exile_area), 1)
