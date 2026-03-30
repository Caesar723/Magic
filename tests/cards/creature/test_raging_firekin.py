from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestRaging_Firekin(CardTestCaseBase):
    async def test_raging_firekin_trample_deals_excess_damage(self):
        card_cls = load_card_class_from_path("pycards/creature/Raging_Firekin/model.py", "Raging_Firekin")
        env = self.make_env()
        card = card_cls(env.p1)
        blocker = env.put_creatures(env.p2, "Small Blocker", 1, 1, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        firekin = env.get_battlefield_creature(env.p1, "Raging Firekin")
        self.assert_state(firekin, {"flags": {"Trample": True}, "state": (3, 2)})

        await env.simulate_combat(firekin, blocker)
        self.assertEqual(env.p2.life, 18)
        self.assertEqual(env.p1.life, 20)

    async def test_raging_firekin_no_trample_damage_when_blocker_absorbs_all(self):
        card_cls = load_card_class_from_path("pycards/creature/Raging_Firekin/model.py", "Raging_Firekin")
        env = self.make_env()
        card = card_cls(env.p1)
        blocker = env.put_creatures(env.p2, "Sturdy Blocker", 2, 5, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        firekin = env.get_battlefield_creature(env.p1, "Raging Firekin")
        before_life = env.p2.life
        await env.simulate_combat(firekin, blocker)
        self.assertEqual(env.p2.life, before_life)

    async def test_raging_firekin_trample_leaves_unblocked_enemy_creature_untouched(self):
        card_cls = load_card_class_from_path("pycards/creature/Raging_Firekin/model.py", "Raging_Firekin")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Bystander", 1, 5, 1)
        blocker = env.put_creatures(env.p2, "Chump", 1, 1, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        firekin = env.get_battlefield_creature(env.p1, "Raging Firekin")
        await env.simulate_combat(firekin, blocker)
        bystander = env.get_battlefield_creature(env.p2, "Bystander")
        self.assertEqual(bystander.state, (1, 5))
