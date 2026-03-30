from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestUnyielding_Resolve(CardTestCaseBase):
    async def test_unyielding_resolve_gives_team_lifelink_and_indestructible(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Unyielding_Resolve/model.py", "Unyielding_Resolve")
        env = self.make_env()
        card = card_cls(env.p1)

        c1 = env.put_creatures(env.p1, "Ally One", 2, 2, 1)[0]
        c2 = env.put_creatures(env.p1, "Ally Two", 3, 3, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertTrue(c1.get_flag("lifelink"))
        self.assertTrue(c2.get_flag("lifelink"))
        self.assert_state(c1, {"buffs_contains": ["Indestructible"]})
        self.assert_state(c2, {"buffs_contains": ["Indestructible"]})

    async def test_unyielding_resolve_does_not_buff_opponent_creatures(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Unyielding_Resolve/model.py", "Unyielding_Resolve")
        env = self.make_env()
        card = card_cls(env.p1)
        ally = env.put_creatures(env.p1, "Ally", 2, 2, 1)[0]
        foe = env.put_creatures(env.p2, "Foe", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assert_state(ally, {"buffs_contains": ["Indestructible"]})
        self.assertNotIn("Indestructible", [type(b).__name__ for b in foe.buffs])
        self.assertFalse(foe.get_flag("lifelink"))

    async def test_unyielding_resolve_empty_battlefield_resolves(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Unyielding_Resolve/model.py", "Unyielding_Resolve")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.battlefield.clear()

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertFalse(env.p1.battlefield)
