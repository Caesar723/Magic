from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestTime_Warp(CardTestCaseBase):
    async def test_time_warp_adds_extra_turn_and_keeps_hand_count(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Time_Warp/model.py", "Time_Warp")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(env.p1, {"counters": {"extra_turn": 1}})
        self.assertEqual(len(env.p1.hand), hand_before)

    async def test_time_warp_empty_library_still_grants_extra_turn(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Time_Warp/model.py", "Time_Warp")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = []
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assert_state(env.p1, {"counters": {"extra_turn": 1}})

    async def test_time_warp_two_casts_stack_extra_turn(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Time_Warp/model.py", "Time_Warp")
        env = self.make_env()
        w1, w2 = card_cls(env.p1), card_cls(env.p1)
        env.p1.library = [Forest(env.p1), Forest(env.p1), Forest(env.p1)]
        env.put_in_hand(w1, env.p1)
        env.put_in_hand(w2, env.p1)
        await env.play_card(w1, env.p1)
        await env.resolve_stack()
        await env.play_card(w2, env.p1)
        await env.resolve_stack()
        self.assert_state(env.p1, {"counters": {"extra_turn": 2}})
