from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestDivine_Sanctuary(CardTestCaseBase):
    async def test_divine_sanctuary_applies_protection_buff(self):
        card_cls = load_card_class_from_path("pycards/Instant/Divine_Sanctuary/model.py", "Divine_Sanctuary")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Protected", 2, 2, 1)[0]
        second = env.put_creatures(env.p1, "Protected Two", 3, 3, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(creature, {"buffs_contains": ["Divine_Sanctuary_Buff"]})
        self.assert_state(second, {"buffs_contains": ["Divine_Sanctuary_Buff"]})

        await creature.take_damage(card, 99, env.p1, env.p2)
        self.assertGreater(creature.state[1], 0)

    async def test_divine_sanctuary_only_affects_friendly_creatures(self):
        card_cls = load_card_class_from_path("pycards/Instant/Divine_Sanctuary/model.py", "Divine_Sanctuary")
        env = self.make_env()
        card = card_cls(env.p1)

        ally = env.put_creatures(env.p1, "Ally", 2, 2, 1)[0]
        enemy = env.put_creatures(env.p2, "Enemy", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(ally, {"buffs_contains": ["Divine_Sanctuary_Buff"]})
        self.assertNotIn("Divine_Sanctuary_Buff", [type(buff).__name__ for buff in enemy.buffs])

    async def test_divine_sanctuary_resolves_with_empty_friendly_battlefield(self):
        card_cls = load_card_class_from_path("pycards/Instant/Divine_Sanctuary/model.py", "Divine_Sanctuary")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.battlefield.clear()

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertFalse(env.p1.battlefield)
