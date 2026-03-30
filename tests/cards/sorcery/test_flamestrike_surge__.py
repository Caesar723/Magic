from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestFlamestrike_Surge__(CardTestCaseBase):
    async def test_flamestrike_surge_hits_target_and_loots(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Flamestrike_Surge__/model.py", "Flamestrike_Surge__")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Strike Target", 2, 3, 1)[0]
        hand_before = len(env.p1.hand)
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotEqual(env.card_zone(target), "battlefield")
        self.assertEqual(len(env.p1.hand), hand_before - 1)

    async def test_flamestrike_surge_can_target_opponent_player(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Flamestrike_Surge__/model.py", "Flamestrike_Surge__")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p2.life = 25
        life_before = env.p2.life
        with patch(
            "game.game_function_tool.random.choice",
            side_effect=lambda seq: env.p2 if env.p2 in seq else seq[0],
        ):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, life_before - 3)

    async def test_flamestrike_surge_controller_life_unchanged_when_creature_dies(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Flamestrike_Surge__/model.py", "Flamestrike_Surge__")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Victim", 2, 3, 1)
        life_before = env.p1.life
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life_before)
