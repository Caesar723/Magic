from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestResurgence(CardTestCaseBase):
    async def test_resurgence_grants_team_buffs_and_reanimates(self):
        card_cls = load_card_class_from_path("pycards/Instant/Resurgence/model.py", "Resurgence")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        ally = env.put_creatures(env.p1, "Ally", 2, 2, 1)[0]
        env.p1.graveyard.append(creature_cls(env.p1))

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(ally, {"buffs_contains": ["DoubleStrike", "Lifelink"]})
        self.assertIsNotNone(env.find_card_by_name(env.p1, "Night Stalker", zones=("battlefield",)))
        self.assertEqual(env.p2.life, 20)

    async def test_resurgence_buffs_without_graveyard_creature(self):
        card_cls = load_card_class_from_path("pycards/Instant/Resurgence/model.py", "Resurgence")
        env = self.make_env()
        card = card_cls(env.p1)

        ally = env.put_creatures(env.p1, "Only Ally", 2, 2, 1)[0]
        env.p1.graveyard.clear()

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(ally, {"buffs_contains": ["DoubleStrike", "Lifelink"]})
        self.assertIsNone(env.find_card_by_name(env.p1, "Night Stalker", zones=("battlefield",)))

    async def test_resurgence_does_not_buff_enemy_creatures(self):
        card_cls = load_card_class_from_path("pycards/Instant/Resurgence/model.py", "Resurgence")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "Ally", 2, 2, 1)
        foe = env.put_creatures(env.p2, "Foe", 3, 3, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertNotIn("DoubleStrike", [type(b).__name__ for b in foe.buffs])
        self.assertNotIn("Lifelink", [type(b).__name__ for b in foe.buffs])
