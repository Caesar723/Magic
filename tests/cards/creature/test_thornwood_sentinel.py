from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestThornwood_Sentinel(CardTestCaseBase):
    async def test_thornwood_sentinel_has_reach(self):
        card_cls = load_card_class_from_path("pycards/creature/Thornwood_Sentinel/model.py", "Thornwood_Sentinel")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        sentinel = env.get_battlefield_creature(env.p1, "Thornwood Sentinel")
        self.assert_state(sentinel, {"zone": "battlefield", "state": (2, 3), "flags": {"reach": True}})

    async def test_thornwood_sentinel_blocks_flying_attacker(self):
        card_cls = load_card_class_from_path("pycards/creature/Thornwood_Sentinel/model.py", "Thornwood_Sentinel")
        env = self.make_env()
        card = card_cls(env.p1)
        flyer = env.put_creatures(env.p2, "Enemy Flyer", 2, 2, 1, flying=True)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        sentinel = env.get_battlefield_creature(env.p1, "Thornwood Sentinel")
        life_before = env.p1.life
        await env.simulate_combat(flyer, sentinel)
        self.assertEqual(env.p1.life, life_before)

    async def test_thornwood_sentinel_unblocked_ground_attacker_damages_player(self):
        card_cls = load_card_class_from_path("pycards/creature/Thornwood_Sentinel/model.py", "Thornwood_Sentinel")
        env = self.make_env()
        card = card_cls(env.p1)
        ground = env.put_creatures(env.p2, "Ground", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        life_before = env.p1.life
        await env.simulate_combat(ground)
        self.assertEqual(env.p1.life, life_before - 2)
