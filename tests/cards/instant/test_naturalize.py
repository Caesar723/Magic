from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestNaturalize(CardTestCaseBase):
    async def test_naturalize_currently_destroys_creature_target(self):
        card_cls = load_card_class_from_path("pycards/Instant/Naturalize/model.py", "Naturalize")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Naturalize Target", 2, 2, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "graveyard")

    async def test_naturalize_player_target_does_not_affect_land(self):
        card_cls = load_card_class_from_path("pycards/Instant/Naturalize/model.py", "Naturalize")
        env = self.make_env()
        card = card_cls(env.p1)

        land = env.p2.hand.pop(0)
        env.p2.land_area.append(land)
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: env.p2 if env.p2 in seq else seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertIn(land, env.p2.land_area)

    async def test_naturalize_opponent_life_unchanged_when_destroying_creature(self):
        card_cls = load_card_class_from_path("pycards/Instant/Naturalize/model.py", "Naturalize")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Naturalize Target", 2, 2, 1)[0]
        opp_before = env.p2.life
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_before)
        self.assertEqual(env.card_zone(target), "graveyard")
