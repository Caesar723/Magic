from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestMystic_Convergence(CardTestCaseBase):
    async def test_mystic_convergence_stores_and_converts_prevented_damage_to_mana(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Convergence/model.py", "Mystic_Convergence")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        card.damage_collect = 5
        mana_before = dict(env.p1.mana)
        await env.trigger(card, "when_start_turn", env.p1, env.p2)

        self.assertFalse(card.get_flag("start_receive"))
        self.assertGreater(sum(env.p1.mana.values()), sum(mana_before.values()))

    async def test_mystic_convergence_no_prevented_damage_adds_no_mana(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Convergence/model.py", "Mystic_Convergence")
        env = self.make_env()
        card = card_cls(env.p1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        card.damage_collect = 0
        mana_before = dict(env.p1.mana)
        await env.trigger(card, "when_start_turn", env.p1, env.p2)
        self.assertEqual(dict(env.p1.mana), mana_before)
        self.assertFalse(card.get_flag("start_receive"))

    async def test_mystic_convergence_upkeep_mana_does_not_affect_opponent(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Convergence/model.py", "Mystic_Convergence")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        card.damage_collect = 10
        opp_mana_before = dict(env.p2.mana)
        await env.trigger(card, "when_start_turn", env.p1, env.p2)

        self.assertEqual(dict(env.p2.mana), opp_mana_before)
