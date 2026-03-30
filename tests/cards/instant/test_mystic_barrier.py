from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestMystic_Barrier(CardTestCaseBase):
    async def test_mystic_barrier_choice_one_grants_hexproof(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Barrier/model.py", "Mystic_Barrier")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Self C", 2, 2, 1)[0]
        creature_two = env.put_creatures(env.p1, "Self C2", 2, 3, 1)[0]
        result = await env.play_card(card, env.p1, selections=[0])
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(creature, {"buffs_contains": ["KeyBuff"]})
        self.assert_state(creature_two, {"buffs_contains": ["KeyBuff"]})

    async def test_mystic_barrier_choice_two_locks_noncreature_spells(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Barrier/model.py", "Mystic_Barrier")
        instant_cls = load_card_class_from_path("pycards/Instant/Swift_Ward/model.py", "Swift_Ward")
        creature_cls = load_card_class_from_path("pycards/creature/Tidal_Sprite/model.py", "Tidal_Sprite")
        env = self.make_env()
        card = card_cls(env.p1)

        noncreature_spell = instant_cls(env.p2)
        creature_spell = creature_cls(env.p2)
        env.p2.hand = [noncreature_spell, creature_spell]

        result = await env.play_card(card, env.p1, selections=[1])
        await env.resolve_stack()

        self.assertTrue(result[0])
        can_cast_noncreature, _ = noncreature_spell.check_can_use(env.p2)
        can_cast_creature, _ = creature_spell.check_can_use(env.p2)
        self.assertFalse(can_cast_noncreature)
        self.assertTrue(can_cast_creature)

    async def test_mystic_barrier_hexproof_branch_does_not_buff_enemy_creatures(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Barrier/model.py", "Mystic_Barrier")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "Ally", 2, 2, 1)
        foe = env.put_creatures(env.p2, "Foe", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1, selections=[0])
        await env.resolve_stack()
        self.assertTrue(result[0])
        ally = env.get_battlefield_creature(env.p1, "Ally")
        self.assertTrue(any(type(b).__name__ == "KeyBuff" for b in ally.buffs))
        self.assertEqual(len(foe.buffs), 0)
