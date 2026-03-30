from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestSwift_Ward(CardTestCaseBase):
    async def test_swift_ward_gives_stats_and_hexproof(self):
        card_cls = load_card_class_from_path("pycards/Instant/Swift_Ward/model.py", "Swift_Ward")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Ward Target", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertGreaterEqual(creature.state[0], 3)
        self.assertTrue(creature.get_flag("Hexproof"))

    async def test_swift_ward_bonus_expires_at_end_turn(self):
        card_cls = load_card_class_from_path("pycards/Instant/Swift_Ward/model.py", "Swift_Ward")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Ward End Turn", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(creature.state, (3, 3))

        for buff in list(creature.buffs):
            if buff.__class__.__name__ in {"StateBuff", "KeyBuff"}:
                buff.when_end_turn()
        self.assertEqual(creature.state, (2, 2))
        self.assertFalse(creature.get_flag("Hexproof"))

    async def test_swift_ward_does_not_grant_hexproof_to_opponent_creature(self):
        card_cls = load_card_class_from_path("pycards/Instant/Swift_Ward/model.py", "Swift_Ward")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_creatures(env.p1, "Warded", 2, 2, 1)
        enemy = env.put_creatures(env.p2, "Exposed", 2, 2, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertFalse(enemy.get_flag("Hexproof"))
