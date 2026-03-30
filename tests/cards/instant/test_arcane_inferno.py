from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestArcane_Inferno(CardTestCaseBase):
    async def test_arcane_inferno_deals_five_with_big_creature(self):
        card_cls = load_card_class_from_path("pycards/Instant/Arcane_Inferno/model.py", "Arcane_Inferno")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_creatures(env.p1, "Big Ally", 5, 5, 1)
        target = env.put_creatures(env.p2, "Inferno Target", 2, 5, 1)[0]
        with patch(
            "game.game_function_tool.random.choice",
            side_effect=lambda seq: target if target in seq else seq[0],
        ):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "graveyard")

    async def test_arcane_inferno_deals_three_without_five_power_ally(self):
        card_cls = load_card_class_from_path("pycards/Instant/Arcane_Inferno/model.py", "Arcane_Inferno")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_creatures(env.p1, "Small Ally", 2, 2, 1)
        target = env.put_creatures(env.p2, "Tough Target", 2, 5, 1)[0]
        with patch(
            "game.game_function_tool.random.choice",
            side_effect=lambda seq: target if target in seq else seq[0],
        ):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(target.state[1], 2)

    async def test_arcane_inferno_can_target_opponent_player_for_three(self):
        card_cls = load_card_class_from_path("pycards/Instant/Arcane_Inferno/model.py", "Arcane_Inferno")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_creatures(env.p1, "Small Ally", 2, 2, 1)
        env.p2.life = 20

        def _pick(seq):
            for item in seq:
                if item is env.p2:
                    return item
            return seq[0]

        with patch("game.game_function_tool.random.choice", side_effect=_pick):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, 17)
