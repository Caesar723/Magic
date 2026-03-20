from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestCelestial_Herald(CardTestCaseBase):
    async def test_celestial_herald_enters_with_keywords(self):
        card_cls = load_card_class_from_path("pycards/creature/Celestial_Herald/model.py", "Celestial_Herald")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        herald = env.get_battlefield_creature(env.p1, "Celestial Herald")

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertTrue(result[0])
        self.assert_state(herald, {
            "zone": "battlefield",
            "state": (3, 3),
            "flags": {"flying": True, "lifelink": True},
        })

    async def test_celestial_herald_upkeep_exiles_one_opponent_creature(self):
        card_cls = load_card_class_from_path("pycards/creature/Celestial_Herald/model.py", "Celestial_Herald")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Test Defender", 2, 2, 2)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        herald = env.get_battlefield_creature(env.p1, "Celestial Herald")

        before = env.snapshot()
        await env.trigger(herald, "when_start_turn", env.p1, env.p2)
        await env.room.check_death()
        after = env.snapshot()

        self.assertEqual(before["p2"]["battlefield"].count("Test Defender"), 2)
        self.assertEqual(after["p2"]["battlefield"].count("Test Defender"), 1)
        self.assertEqual(after["p2"]["exile_count"], 1)
        self.assertIsNot(herald.creature_store, False)
        self.assertEqual(getattr(herald.creature_store, "name", ""), "Test Defender")

    async def test_celestial_herald_second_upkeep_returns_previous_and_exiles_new(self):
        card_cls = load_card_class_from_path("pycards/creature/Celestial_Herald/model.py", "Celestial_Herald")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Test Defender", 2, 2, 2)
        env.p1.life = 15

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        herald = env.get_battlefield_creature(env.p1, "Celestial Herald")

        # First upkeep: exile one.
        await env.trigger(herald, "when_start_turn", env.p1, env.p2)
        await env.room.check_death()
        first_exiled = herald.creature_store
        after_first = env.snapshot()
        self.assertEqual(after_first["p2"]["battlefield"].count("Test Defender"), 1)
        self.assertEqual(after_first["p2"]["exile_count"], 1)

        # Second upkeep: return previous, exile current.
        await env.trigger(herald, "when_start_turn", env.p1, env.p2)
        await env.room.check_death()
        second_exiled = herald.creature_store
        after_second = env.snapshot()

        self.assertIsNot(first_exiled, second_exiled)
        self.assertEqual(after_second["p2"]["battlefield"].count("Test Defender"), 1)
        self.assertEqual(after_second["p2"]["exile_count"], 1)

        # Lifelink sanity: hit opponent directly and gain life.
        before_life = env.snapshot()
        await env.simulate_combat(herald)
        after_life = env.snapshot()
        self.assertEqual(after_life["p2"]["life"], before_life["p2"]["life"] - 3)
        self.assertGreaterEqual(after_life["p1"]["life"], before_life["p1"]["life"])
