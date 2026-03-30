from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestIronclad_Crusader(CardTestCaseBase):
    async def test_ironclad_crusader_etb_taps_enemy_creature(self):
        card_cls = load_card_class_from_path("pycards/creature/Ironclad_Crusader/model.py", "Ironclad_Crusader")
        env = self.make_env()
        card = card_cls(env.p1)

        enemy = env.put_creatures(env.p2, "Enemy Target", 2, 2, 1)[0]
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        crusader = env.get_battlefield_creature(env.p1, "Ironclad Crusader")
        self.assert_state(crusader, {"zone": "battlefield", "state": (2, 2)})
        self.assertTrue(enemy.get_flag("tap"))

    async def test_ironclad_crusader_taps_second_enemy_when_random_picks_it(self):
        card_cls = load_card_class_from_path("pycards/creature/Ironclad_Crusader/model.py", "Ironclad_Crusader")
        env = self.make_env()
        card = card_cls(env.p1)

        a = env.put_creatures(env.p2, "Enemy A", 1, 1, 1)[0]
        b = env.put_creatures(env.p2, "Enemy B", 2, 2, 1)[0]

        with patch("game.game_function_tool.random.choice", side_effect=lambda s: s[1]):
            result = await env.play_card(card, env.p1)
            await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertFalse(a.get_flag("tap"))
        self.assertTrue(b.get_flag("tap"))

    async def test_ironclad_crusader_fails_play_without_opponent_creature_target(self):
        card_cls = load_card_class_from_path("pycards/creature/Ironclad_Crusader/model.py", "Ironclad_Crusader")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p2.battlefield.clear()
        result = await env.play_card(card, env.p1)
        self.assertFalse(result[0])
        self.assertIn(card, env.p1.hand)
        self.assertEqual(len(env.p1.battlefield), 0)
