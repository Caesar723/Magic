from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestSpectral_Embrace(CardTestCaseBase):
    async def test_spectral_embrace_buffs_and_grants_indestructible(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Spectral_Embrace/model.py", "Spectral_Embrace")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Self C", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertGreaterEqual(creature.state[0], 4)
        self.assertGreaterEqual(creature.state[1], 4)
        self.assert_state(creature, {"buffs_contains": ["Indestructible"]})

    async def test_spectral_embrace_hits_all_allies_and_skips_enemy_creatures(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Spectral_Embrace/model.py", "Spectral_Embrace")
        env = self.make_env()
        card = card_cls(env.p1)
        a1 = env.put_creatures(env.p1, "Ally One", 1, 3, 1)[0]
        a2 = env.put_creatures(env.p1, "Ally Two", 2, 1, 1)[0]
        enemy = env.put_creatures(env.p2, "Enemy", 2, 2, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        self.assertEqual(a1.state, (3, 5))
        self.assertEqual(a2.state, (4, 3))
        self.assertEqual(enemy.state, (2, 2))
        self.assert_state(a1, {"buffs_contains": ["Indestructible"]})
        self.assert_state(a2, {"buffs_contains": ["Indestructible"]})
        self.assertNotIn("Indestructible", [type(b).__name__ for b in enemy.buffs])

    async def test_spectral_embrace_does_not_change_opponent_life(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Spectral_Embrace/model.py", "Spectral_Embrace")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "Lonely", 2, 2, 1)
        opp_life = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_life)
