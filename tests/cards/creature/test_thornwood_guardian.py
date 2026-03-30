from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestThornwood_Guardian(CardTestCaseBase):
    async def test_thornwood_guardian_keywords(self):
        card_cls = load_card_class_from_path("pycards/creature/Thornwood_Guardian/model.py", "Thornwood_Guardian")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        guardian = env.get_battlefield_creature(env.p1, "Thornwood Guardian")
        self.assert_state(guardian, {
            "zone": "battlefield",
            "state": (5, 4),
            "flags": {"reach": True, "Trample": True},
        })

    async def test_thornwood_guardian_trample_deals_excess(self):
        card_cls = load_card_class_from_path("pycards/creature/Thornwood_Guardian/model.py", "Thornwood_Guardian")
        env = self.make_env()
        card = card_cls(env.p1)
        blocker = env.put_creatures(env.p2, "Tiny Blocker", 1, 1, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        guardian = env.get_battlefield_creature(env.p1, "Thornwood Guardian")
        await env.simulate_combat(guardian, blocker)
        self.assertEqual(env.p2.life, 16)

    async def test_thornwood_guardian_unblocked_hits_player_for_full_power(self):
        card_cls = load_card_class_from_path("pycards/creature/Thornwood_Guardian/model.py", "Thornwood_Guardian")
        env = self.make_env()
        card = card_cls(env.p1)
        life_before = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        guardian = env.get_battlefield_creature(env.p1, "Thornwood Guardian")
        await env.simulate_combat(guardian)
        self.assertEqual(env.p2.life, life_before - guardian.state[0])
