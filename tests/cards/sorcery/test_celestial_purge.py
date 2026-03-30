from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestCelestial_Purge(CardTestCaseBase):
    async def test_celestial_purge_exiles_red_or_black_target(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Celestial_Purge/model.py", "Celestial_Purge")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Red Target", 2, 2, 1)[0]
        target.color = "red"

        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "exile_area")

    async def test_celestial_purge_non_red_black_creature_not_exiled(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Celestial_Purge/model.py", "Celestial_Purge")
        env = self.make_env()
        card = card_cls(env.p1)
        target = env.put_creatures(env.p2, "Green One", 2, 2, 1)[0]
        target.color = "green"

        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "battlefield")

    async def test_celestial_purge_controller_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Celestial_Purge/model.py", "Celestial_Purge")
        env = self.make_env()
        card = card_cls(env.p1)
        t = env.put_creatures(env.p2, "Black One", 2, 2, 1)[0]
        t.color = "black"
        ctrl_life = env.p1.life

        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, ctrl_life)
