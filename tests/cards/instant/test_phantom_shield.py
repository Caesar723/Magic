from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestPhantom_Shield(CardTestCaseBase):
    async def test_phantom_shield_applies_prevent_damage_buff(self):
        card_cls = load_card_class_from_path("pycards/Instant/Phantom_Shield/model.py", "Phantom_Shield")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Shielded", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(creature, {"buffs_contains": ["Phantom_Shield_Buff"]})

        life_before = creature.state[1]
        await creature.take_damage(card, 5, env.p1, env.p2)
        self.assertEqual(creature.state[1], life_before)

    async def test_phantom_shield_buffs_all_friendly_creatures(self):
        card_cls = load_card_class_from_path("pycards/Instant/Phantom_Shield/model.py", "Phantom_Shield")
        env = self.make_env()
        card = card_cls(env.p1)

        first = env.put_creatures(env.p1, "Shielded A", 2, 2, 1)[0]
        second = env.put_creatures(env.p1, "Shielded B", 3, 3, 1)[0]
        enemy = env.put_creatures(env.p2, "Enemy", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(first, {"buffs_contains": ["Phantom_Shield_Buff"]})
        self.assert_state(second, {"buffs_contains": ["Phantom_Shield_Buff"]})
        self.assertNotIn("Phantom_Shield_Buff", [type(buff).__name__ for buff in enemy.buffs])

    async def test_phantom_shield_does_not_change_opponent_life(self):
        card_cls = load_card_class_from_path("pycards/Instant/Phantom_Shield/model.py", "Phantom_Shield")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "Ally", 2, 2, 1)
        opp_before = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_before)
