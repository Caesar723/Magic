from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestEphemeral_Insight(CardTestCaseBase):
    async def test_ephemeral_insight_draws_and_returns_once(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ephemeral_Insight/model.py", "Ephemeral_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 2)
        self.assertTrue(any(c.name == "Ephemeral Insight" for c in env.p1.hand))
        self.assertEqual(env.p2.life, 20)

    async def test_ephemeral_insight_been_used_copy_draws_only_once_more(self):
        """Second instance has `been used` set; resolving it does not add another copy to hand."""
        card_cls = load_card_class_from_path("pycards/Instant/Ephemeral_Insight/model.py", "Ephemeral_Insight")
        env = self.make_env()
        first = card_cls(env.p1)
        env.p1.library = [Forest(env.p1), Forest(env.p1)]

        result = await env.play_card(first, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        second = next(c for c in env.p1.hand if c.name == "Ephemeral Insight")
        self.assertTrue(second.get_flag("been used"))
        hand_before_second = len(env.p1.hand)

        result2 = await env.play_card(second, env.p1)
        await env.resolve_stack()
        self.assertTrue(result2[0])
        self.assertEqual(len(env.p1.hand), hand_before_second)
        self.assertFalse(any(c.name == "Ephemeral Insight" for c in env.p1.hand))

    async def test_ephemeral_insight_opponent_hand_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ephemeral_Insight/model.py", "Ephemeral_Insight")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1), Forest(env.p1)]
        opp_hand_before = len(env.p2.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.hand), opp_hand_before)
