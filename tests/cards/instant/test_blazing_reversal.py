from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestBlazing_Reversal(CardTestCaseBase):
    async def test_blazing_reversal_draws_a_card(self):
        card_cls = load_card_class_from_path("pycards/Instant/Blazing_Reversal/model.py", "Blazing_Reversal")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)

    async def test_blazing_reversal_no_library_no_extra_card(self):
        card_cls = load_card_class_from_path("pycards/Instant/Blazing_Reversal/model.py", "Blazing_Reversal")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = []
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before)

    async def test_blazing_reversal_does_not_draw_for_opponent(self):
        card_cls = load_card_class_from_path("pycards/Instant/Blazing_Reversal/model.py", "Blazing_Reversal")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1)]
        opp_hand_before = len(env.p2.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.hand), opp_hand_before)
