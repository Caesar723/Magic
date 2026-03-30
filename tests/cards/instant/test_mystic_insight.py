from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest
from unittest.mock import AsyncMock


class TestMystic_Insight(CardTestCaseBase):
    async def test_mystic_insight_scry_three_then_draw(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Insight/model.py", "Mystic_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)

    async def test_mystic_insight_calls_scry_three(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Insight/model.py", "Mystic_Insight")
        env = self.make_env()
        card = card_cls(env.p1)
        card.Scry = AsyncMock(return_value=None)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        card.Scry.assert_awaited_once_with(env.p1, env.p2, 3)

    async def test_mystic_insight_does_not_change_opponent_hand(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Insight/model.py", "Mystic_Insight")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1)]
        opp_before = len(env.p2.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.hand), opp_before)
