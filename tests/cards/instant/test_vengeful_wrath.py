from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestVengeful_Wrath(CardTestCaseBase):
    async def test_vengeful_wrath_destroys_target_creature(self):
        card_cls = load_card_class_from_path("pycards/Instant/Vengeful_Wrath/model.py", "Vengeful_Wrath")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Wrath Target", 3, 3, 1)[0]
        env.put_creatures(env.p2, "Other", 2, 2, 1)
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "graveyard")

    async def test_vengeful_wrath_no_random_followup_when_only_one_opponent_creature(self):
        card_cls = load_card_class_from_path("pycards/Instant/Vengeful_Wrath/model.py", "Vengeful_Wrath")
        env = self.make_env()
        card = card_cls(env.p1)

        lone = env.put_creatures(env.p2, "Only Opp", 2, 5, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(lone), "graveyard")
        self.assertEqual(len(env.p2.battlefield), 0)

    async def test_vengeful_wrath_controller_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Vengeful_Wrath/model.py", "Vengeful_Wrath")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "T", 3, 3, 1)
        life = env.p1.life
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life)
