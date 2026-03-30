from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestCelestial_Renewal(CardTestCaseBase):
    async def test_celestial_renewal_returns_all_creatures_from_graveyard(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Celestial_Renewal/model.py", "Celestial_Renewal")
        env = self.make_env()
        card = card_cls(env.p1)

        dead1 = env.create_creature(env.p1, "Dead One", 2, 2)
        dead2 = env.create_creature(env.p1, "Dead Two", 3, 3)
        env.p1.graveyard.extend([dead1, dead2])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertIn(dead1, env.p1.battlefield)
        self.assertIn(dead2, env.p1.battlefield)

    async def test_celestial_renewal_empty_graveyard_resolves(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Celestial_Renewal/model.py", "Celestial_Renewal")
        env = self.make_env()
        card = card_cls(env.p1)
        self.assertFalse(env.p1.graveyard)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertFalse(env.p1.battlefield)

    async def test_celestial_renewal_does_not_return_opponent_graveyard_creatures(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Celestial_Renewal/model.py", "Celestial_Renewal")
        env = self.make_env()
        card = card_cls(env.p1)

        own_dead = env.create_creature(env.p1, "Mine", 2, 2)
        opp_dead = env.create_creature(env.p2, "Theirs", 1, 1)
        env.p1.graveyard.append(own_dead)
        env.p2.graveyard.append(opp_dead)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertIn(own_dead, env.p1.battlefield)
        self.assertIn(opp_dead, env.p2.graveyard)
        self.assertNotIn(opp_dead, env.p1.battlefield)
