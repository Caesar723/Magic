from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestCelestial_Seraph(CardTestCaseBase):
    async def test_celestial_seraph_enters_with_flying_lifelink(self):
        card_cls = load_card_class_from_path("pycards/creature/Celestial_Seraph/model.py", "Celestial_Seraph")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        seraph = env.get_battlefield_creature(env.p1, "Celestial Seraph")
        self.assert_state(seraph, {
            "zone": "battlefield",
            "state": (5, 5),
            "flags": {"flying": True, "lifelink": True},
        })

    async def test_celestial_seraph_attack_exiles_and_leave_returns(self):
        card_cls = load_card_class_from_path("pycards/creature/Celestial_Seraph/model.py", "Celestial_Seraph")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Test Defender", 2, 2, 2)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        seraph = env.get_battlefield_creature(env.p1, "Celestial Seraph")

        before = env.snapshot()
        await env.simulate_combat(seraph)
        await env.room.check_death()
        after_attack = env.snapshot()
        self.assertEqual(after_attack["p2"]["battlefield"].count("Test Defender"), 1)
        self.assertEqual(after_attack["p2"]["exile_count"], 1)
        self.assertEqual(after_attack["p2"]["life"], before["p2"]["life"] - 5)

        await env.move_to_graveyard(seraph)
        after_leave = env.snapshot()
        self.assertEqual(after_leave["p2"]["battlefield"].count("Test Defender"), 2)

    async def test_celestial_seraph_attack_with_empty_opponent_battlefield_exiles_nothing(self):
        card_cls = load_card_class_from_path("pycards/creature/Celestial_Seraph/model.py", "Celestial_Seraph")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p2.battlefield.clear()

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        seraph = env.get_battlefield_creature(env.p1, "Celestial Seraph")

        before = env.snapshot()
        await env.simulate_combat(seraph)
        await env.room.check_death()
        after = env.snapshot()

        self.assertEqual(after["p2"]["exile_count"], before["p2"]["exile_count"])
        self.assertEqual(seraph.creature_store, [])
        self.assertEqual(after["p2"]["life"], before["p2"]["life"] - 5)
