from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestHarbinger_of_the_Eternal_Tides(CardTestCaseBase):
    async def test_harbinger_has_flash_and_taps_enemy_on_etb(self):
        card_cls = load_card_class_from_path("pycards/creature/Harbinger_of_the_Eternal_Tides/model.py", "Harbinger_of_the_Eternal_Tides")
        env = self.make_env()
        card = card_cls(env.p1)

        enemy = env.put_creatures(env.p2, "Enemy Target", 2, 2, 1)[0]
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        harbinger = env.get_battlefield_creature(env.p1, "Harbinger of the Eternal Tides")
        self.assert_state(harbinger, {
            "zone": "battlefield",
            "state": (2, 4),
            "flags": {"Flash": True},
        })
        self.assertTrue(enemy.get_flag("tap"))

    async def test_harbinger_taps_second_enemy_when_random_targets_it(self):
        card_cls = load_card_class_from_path("pycards/creature/Harbinger_of_the_Eternal_Tides/model.py", "Harbinger_of_the_Eternal_Tides")
        env = self.make_env()
        card = card_cls(env.p1)

        first = env.put_creatures(env.p2, "Enemy A", 1, 1, 1)[0]
        second = env.put_creatures(env.p2, "Enemy B", 2, 2, 1)[0]

        with patch("game.game_function_tool.random.choice", side_effect=lambda s: s[1]):
            result = await env.play_card(card, env.p1)
            await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertFalse(first.get_flag("tap"))
        self.assertTrue(second.get_flag("tap"))

    async def test_harbinger_cannot_cast_when_opponent_has_no_creatures(self):
        card_cls = load_card_class_from_path("pycards/creature/Harbinger_of_the_Eternal_Tides/model.py", "Harbinger_of_the_Eternal_Tides")
        env = self.make_env()
        card = card_cls(env.p1)
        self.assertFalse(env.p2.battlefield)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertFalse(result[0])
        self.assertIn(card, env.p1.hand)
