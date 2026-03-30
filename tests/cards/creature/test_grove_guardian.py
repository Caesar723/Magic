from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestGrove_Guardian(CardTestCaseBase):
    async def test_grove_guardian_has_reach_and_hexproof(self):
        card_cls = load_card_class_from_path("pycards/creature/Grove_Guardian/model.py", "Grove_Guardian")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        guardian = env.get_battlefield_creature(env.p1, "Grove Guardian")
        self.assert_state(guardian, {
            "zone": "battlefield",
            "state": (3, 5),
            "flags": {"reach": True, "Hexproof": True},
        })

    async def test_grove_guardian_can_block_flying(self):
        card_cls = load_card_class_from_path("pycards/creature/Grove_Guardian/model.py", "Grove_Guardian")
        env = self.make_env()
        card = card_cls(env.p1)
        flyer = env.put_creatures(env.p2, "Enemy Flyer", 2, 2, 1, flying=True)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        guardian = env.get_battlefield_creature(env.p1, "Grove Guardian")
        life_before = env.p1.life
        await env.simulate_combat(flyer, guardian)
        self.assertEqual(env.p1.life, life_before)

    async def test_grove_guardian_attack_reduces_opponent_life_when_unblocked(self):
        card_cls = load_card_class_from_path("pycards/creature/Grove_Guardian/model.py", "Grove_Guardian")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        guardian = env.get_battlefield_creature(env.p1, "Grove Guardian")
        before = env.p2.life
        await env.simulate_combat(guardian)
        self.assertEqual(env.p2.life, before - 3)

    async def test_grove_guardian_blocked_by_large_creature_does_not_damage_player(self):
        card_cls = load_card_class_from_path("pycards/creature/Grove_Guardian/model.py", "Grove_Guardian")
        env = self.make_env()
        card = card_cls(env.p1)
        wall = env.put_creatures(env.p2, "Huge Wall", 3, 10, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        guardian = env.get_battlefield_creature(env.p1, "Grove Guardian")
        life_before = env.p2.life
        await env.simulate_combat(guardian, wall)
        self.assertEqual(env.p2.life, life_before)
        self.assert_state(wall, {"zone": "battlefield"})
