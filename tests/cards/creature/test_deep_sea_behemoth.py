from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestDeep_Sea_Behemoth(CardTestCaseBase):
    async def test_deep_sea_behemoth_etb_steals_creature_and_returns_on_death(self):
        card_cls = load_card_class_from_path("pycards/creature/Deep_Sea_Behemoth/model.py", "Deep_Sea_Behemoth")
        env = self.make_env()
        card = card_cls(env.p1)

        stolen = env.put_creatures(env.p2, "Enemy Target", 2, 2, 1)[0]
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        behemoth = env.get_battlefield_creature(env.p1, "Deep Sea Behemoth")
        self.assertIn(stolen, env.p1.battlefield)
        self.assertNotIn(stolen, env.p2.battlefield)

        await env.move_to_graveyard(behemoth)
        await env.resolve_stack()
        self.assertIn(stolen, env.p2.battlefield)

    async def test_deep_sea_behemoth_steals_scripted_second_creature(self):
        card_cls = load_card_class_from_path("pycards/creature/Deep_Sea_Behemoth/model.py", "Deep_Sea_Behemoth")
        env = self.make_env()
        card = card_cls(env.p1)

        a = env.put_creatures(env.p2, "First Fish", 1, 1, 1)[0]
        b = env.put_creatures(env.p2, "Second Fish", 3, 3, 1)[0]

        def _pick_second(seq):
            self.assertGreaterEqual(len(seq), 2)
            return seq[1]

        with patch("game.game_function_tool.random.choice", side_effect=_pick_second):
            result = await env.play_card(card, env.p1)
            await env.resolve_stack()
        self.assertTrue(result[0])

        self.assertIn(a, env.p2.battlefield)
        self.assertIn(b, env.p1.battlefield)
        self.assertNotIn(b, env.p2.battlefield)

    async def test_deep_sea_behemoth_fails_play_without_opponent_creature_to_steal(self):
        card_cls = load_card_class_from_path("pycards/creature/Deep_Sea_Behemoth/model.py", "Deep_Sea_Behemoth")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p2.battlefield.clear()
        result = await env.play_card(card, env.p1)
        self.assertFalse(result[0])
        self.assertIn(card, env.p1.hand)
        self.assertEqual(len(env.p1.battlefield), 0)
