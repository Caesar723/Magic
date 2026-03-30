from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestThunderclap_Behemoth(CardTestCaseBase):
    async def test_thunderclap_behemoth_has_trample(self):
        card_cls = load_card_class_from_path("pycards/creature/Thunderclap_Behemoth/model.py", "Thunderclap_Behemoth")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        behemoth = env.get_battlefield_creature(env.p1, "Thunderclap Behemoth")
        self.assert_state(behemoth, {"zone": "battlefield", "state": (6, 6), "flags": {"Trample": True}})

    async def test_thunderclap_behemoth_attack_trigger_scales_trample_damage(self):
        card_cls = load_card_class_from_path("pycards/creature/Thunderclap_Behemoth/model.py", "Thunderclap_Behemoth")
        env = self.make_env()
        card = card_cls(env.p1)

        ally = env.put_creatures(env.p1, "Big Ally", 4, 4, 1)[0]
        defender = env.put_creatures(env.p2, "Defender", 2, 4, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        behemoth = env.get_battlefield_creature(env.p1, "Thunderclap Behemoth")
        await env.simulate_combat(behemoth, defender)
        self.assertEqual(env.p2.life, 15)
        self.assertEqual(ally.state[0], 4)

    async def test_thunderclap_behemoth_no_attack_trigger_when_attacking_alone(self):
        """Requires another creature with power >= 4; Behemoth is skipped when counting."""
        card_cls = load_card_class_from_path("pycards/creature/Thunderclap_Behemoth/model.py", "Thunderclap_Behemoth")
        env = self.make_env()
        card = card_cls(env.p1)
        defender = env.put_creatures(env.p2, "Solo Defender", 2, 4, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        behemoth = env.get_battlefield_creature(env.p1, "Thunderclap Behemoth")
        await env.simulate_combat(behemoth, defender)
        self.assertEqual(env.p2.life, 18)
        self.assertEqual(env.card_zone(defender), "graveyard")

    async def test_thunderclap_behemoth_no_attack_trigger_when_ally_below_four_power(self):
        """Another creature on board with power 3 does not satisfy the condition."""
        card_cls = load_card_class_from_path("pycards/creature/Thunderclap_Behemoth/model.py", "Thunderclap_Behemoth")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "Small Ally", 3, 3, 1)
        defender = env.put_creatures(env.p2, "Blocker", 2, 4, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        behemoth = env.get_battlefield_creature(env.p1, "Thunderclap Behemoth")
        await env.simulate_combat(behemoth, defender)
        self.assertEqual(env.p2.life, 18)
        self.assertEqual(env.card_zone(defender), "graveyard")
