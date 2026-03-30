from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestPhantasmal_Distortion(CardTestCaseBase):
    async def test_phantasmal_distortion_buffs_target_creature(self):
        card_cls = load_card_class_from_path("pycards/Instant/Phantasmal_Distortion/model.py", "Phantasmal_Distortion")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Target", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertGreaterEqual(creature.state[0], 5)
        self.assertGreaterEqual(creature.state[1], 5)

    async def test_phantasmal_distortion_buff_expires_end_turn(self):
        card_cls = load_card_class_from_path("pycards/Instant/Phantasmal_Distortion/model.py", "Phantasmal_Distortion")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Distort Target", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(creature.state, (5, 5))

        state_buffs = [b for b in creature.buffs if b.__class__.__name__ == "StateBuff"]
        self.assertEqual(len(state_buffs), 1)
        state_buffs[0].when_end_turn()
        self.assertEqual(creature.state, (2, 2))

    async def test_phantasmal_distortion_does_not_buff_opponent_creature(self):
        card_cls = load_card_class_from_path("pycards/Instant/Phantasmal_Distortion/model.py", "Phantasmal_Distortion")
        env = self.make_env()
        card = card_cls(env.p1)

        friendly = env.put_creatures(env.p1, "Ally", 2, 2, 1)[0]
        enemy = env.put_creatures(env.p2, "Enemy", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertGreaterEqual(friendly.state[0], 5)
        self.assertEqual(enemy.state, (2, 2))
