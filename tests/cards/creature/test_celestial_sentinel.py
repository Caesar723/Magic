from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestCelestial_Sentinel(CardTestCaseBase):
    async def test_celestial_sentinel_enters_with_flying_and_vigilance(self):
        card_cls = load_card_class_from_path("pycards/creature/Celestial_Sentinel/model.py", "Celestial_Sentinel")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        sentinel = env.get_battlefield_creature(env.p1, "Celestial Sentinel")
        self.assert_state(sentinel, {
            "zone": "battlefield",
            "state": (2, 3),
            "flags": {"flying": True, "Vigilance": True},
        })

    async def test_celestial_sentinel_vigilance_keeps_it_untapped_after_combat(self):
        card_cls = load_card_class_from_path("pycards/creature/Celestial_Sentinel/model.py", "Celestial_Sentinel")
        env = self.make_env()
        card = card_cls(env.p1)
        defenders = env.put_creatures(env.p2, "Test Defender", 2, 2, 1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        sentinel = env.get_battlefield_creature(env.p1, "Celestial Sentinel")
        await env.simulate_combat(sentinel, defenders[0])
        self.assertFalse(sentinel.get_flag("tap"))
        self.assertEqual(env.p2.life, 20)  # blocked by defender

    async def test_celestial_sentinel_unblocked_hits_opponent_life(self):
        card_cls = load_card_class_from_path("pycards/creature/Celestial_Sentinel/model.py", "Celestial_Sentinel")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        sentinel = env.get_battlefield_creature(env.p1, "Celestial Sentinel")

        await env.simulate_combat(sentinel)
        self.assertEqual(env.p2.life, 18)
        self.assertFalse(sentinel.get_flag("tap"))

    async def test_celestial_sentinel_blocks_enemy_attacker_and_survives(self):
        card_cls = load_card_class_from_path("pycards/creature/Celestial_Sentinel/model.py", "Celestial_Sentinel")
        env = self.make_env()
        card = card_cls(env.p1)
        aggressor = env.put_creatures(env.p2, "Small Raider", 1, 1, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        sentinel = env.get_battlefield_creature(env.p1, "Celestial Sentinel")

        p1_life = env.p1.life
        await env.simulate_combat(aggressor, sentinel)
        await env.room.check_death()

        self.assertEqual(env.p1.life, p1_life)
        self.assertEqual(env.card_zone(aggressor), "graveyard")
        self.assert_state(sentinel, {"zone": "battlefield", "state": (2, 2)})
