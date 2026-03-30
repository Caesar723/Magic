from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestPrimal_Surge(CardTestCaseBase):
    async def test_primal_surge_shuffles_hand_and_grants_extra_land_play(self):
        card_cls = load_card_class_from_path("pycards/Instant/Primal_Surge/model.py", "Primal_Surge")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.hand.append(Forest(env.p1))
        before = env.p1.get_counter_from_dict("lands_summon_max")
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.get_counter_from_dict("lands_summon_max"), before + 1)

    async def test_primal_surge_reverts_land_counter_at_end_turn(self):
        card_cls = load_card_class_from_path("pycards/Instant/Primal_Surge/model.py", "Primal_Surge")
        env = self.make_env()
        card = card_cls(env.p1)

        before = env.p1.get_counter_from_dict("lands_summon_max")
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        await env.trigger(card, "when_end_turn", env.p1, env.p2)

        self.assertTrue(result[0])
        self.assertEqual(env.p1.get_counter_from_dict("lands_summon_max"), before)

    async def test_primal_surge_does_not_raise_opponent_land_play_cap(self):
        card_cls = load_card_class_from_path("pycards/Instant/Primal_Surge/model.py", "Primal_Surge")
        env = self.make_env()
        card = card_cls(env.p1)
        opp_before = env.p2.get_counter_from_dict("lands_summon_max")
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.get_counter_from_dict("lands_summon_max"), opp_before)
