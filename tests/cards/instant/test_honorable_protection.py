from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestHonorable_Protection(CardTestCaseBase):
    async def test_honorable_protection_grants_indestructible(self):
        card_cls = load_card_class_from_path("pycards/Instant/Honorable_Protection/model.py", "Honorable_Protection")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Knight Ally", 2, 2, 1)[0]
        creature.type_card = "Knight"
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(creature, {"buffs_contains": ["Indestructible"]})
        self.assertGreaterEqual(creature.state[0], 3)
        self.assertGreaterEqual(creature.state[1], 3)

    async def test_honorable_protection_non_knight_gets_no_bonus_counter(self):
        card_cls = load_card_class_from_path("pycards/Instant/Honorable_Protection/model.py", "Honorable_Protection")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Generic Ally", 2, 2, 1)[0]
        creature.type_card = "Warrior"
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(creature, {"buffs_contains": ["Indestructible"]})
        self.assertEqual(creature.state[0], 2)
        self.assertEqual(creature.state[1], 2)

    async def test_honorable_protection_does_not_affect_opponent_creatures(self):
        card_cls = load_card_class_from_path("pycards/Instant/Honorable_Protection/model.py", "Honorable_Protection")
        env = self.make_env()
        card = card_cls(env.p1)

        ours = env.put_creatures(env.p1, "Knight Ally", 2, 2, 1)[0]
        ours.type_card = "Knight"
        theirs = env.put_creatures(env.p2, "Enemy Knight", 2, 2, 1)[0]
        theirs.type_card = "Knight"

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(ours, {"buffs_contains": ["Indestructible"]})
        self.assertEqual(theirs.buffs, [])
        self.assertEqual(theirs.state, (2, 2))
