from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestCelestial_Guardian(CardTestCaseBase):
    async def test_celestial_guardian_keywords_and_vigilance_attack(self):
        guardian_cls = load_card_class_from_path("pycards/creature/Celestial_Guardian/model.py", "Celestial_Guardian")
        env = self.make_env()
        card = guardian_cls(env.p1)
        env.p1.life = 15  # below ini_life cap so ETB +2 life is observable

        before_life = env.p1.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, before_life + 2)

        guardian = env.get_battlefield_creature(env.p1, "Celestial Guardian")
        self.assert_state(guardian, {
            "zone": "battlefield",
            "state": (3, 3),
            "flags": {"flying": True, "Vigilance": True},
        })

        await env.simulate_combat(guardian)
        self.assertEqual(env.p2.life, 17)
        self.assertFalse(guardian.get_flag("tap"))

    async def test_celestial_guardian_etb_life_gain_does_not_affect_opponent(self):
        guardian_cls = load_card_class_from_path("pycards/creature/Celestial_Guardian/model.py", "Celestial_Guardian")
        env = self.make_env()
        card = guardian_cls(env.p1)
        env.p1.life = 15
        opp_life = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_life)

    async def test_celestial_guardian_blocked_attack_does_not_damage_opponent(self):
        guardian_cls = load_card_class_from_path("pycards/creature/Celestial_Guardian/model.py", "Celestial_Guardian")
        env = self.make_env()
        card = guardian_cls(env.p1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        guardian = env.get_battlefield_creature(env.p1, "Celestial Guardian")
        wall = env.put_creatures(env.p2, "Wall", 1, 10, 1)[0]
        opp_life = env.p2.life
        await env.simulate_combat(guardian, wall)
        self.assertEqual(env.p2.life, opp_life)
        self.assertEqual(env.card_zone(wall), "battlefield")
