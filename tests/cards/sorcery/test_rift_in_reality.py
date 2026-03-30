from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestRift_in_Reality(CardTestCaseBase):
    async def test_rift_in_reality_exiles_target_permanent(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Rift_in_Reality/model.py", "Rift_in_Reality")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Rift Target", 2, 2, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "exile_area")
        self.assertEqual(env.p1.life, 20)

    async def test_rift_in_reality_exiles_second_creature_when_two_on_opponent_board(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Rift_in_Reality/model.py", "Rift_in_Reality")
        env = self.make_env()
        card = card_cls(env.p1)
        a = env.put_creatures(env.p2, "Rift A", 1, 4, 1)[0]
        b = env.put_creatures(env.p2, "Rift B", 1, 4, 1)[0]

        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: b if b in seq else seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(a), "battlefield")
        self.assertEqual(env.card_zone(b), "exile_area")

    async def test_rift_in_reality_opponent_life_unchanged_when_exiling_creature(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Rift_in_Reality/model.py", "Rift_in_Reality")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Solo", 2, 2, 1)
        opp_before = env.p2.life

        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_before)
