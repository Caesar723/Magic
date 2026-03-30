from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestIcy_Imprisonment(CardTestCaseBase):
    async def test_icy_imprisonment_freezes_all_enemy_creatures(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Icy_Imprisonment/model.py", "Icy_Imprisonment")
        env = self.make_env()
        card = card_cls(env.p1)

        e1 = env.put_creatures(env.p2, "Enemy A", 2, 2, 1)[0]
        e2 = env.put_creatures(env.p2, "Enemy B", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(e1, {"buffs_contains": ["Frozen"]})
        self.assert_state(e2, {"buffs_contains": ["Frozen"]})

    async def test_icy_imprisonment_no_enemy_creatures_is_safe(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Icy_Imprisonment/model.py", "Icy_Imprisonment")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p2.battlefield = []
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])

    async def test_icy_imprisonment_does_not_freeze_friendly_creatures(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Icy_Imprisonment/model.py", "Icy_Imprisonment")
        env = self.make_env()
        card = card_cls(env.p1)
        friend = env.put_creatures(env.p1, "Friend", 2, 2, 1)[0]
        env.put_creatures(env.p2, "Enemy", 2, 2, 1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotIn("Frozen", [type(b).__name__ for b in friend.buffs])
