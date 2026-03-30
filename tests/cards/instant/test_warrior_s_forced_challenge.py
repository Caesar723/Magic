from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestWarrior_s_Forced_Challenge(CardTestCaseBase):
    async def test_warrior_s_forced_challenge_forces_fight_after_counter(self):
        card_cls = load_card_class_from_path("pycards/Instant/Warrior_s_Forced_Challenge/model.py", "Warrior_s_Forced_Challenge")
        env = self.make_env()
        card = card_cls(env.p1)

        ally = env.put_creatures(env.p1, "Ally", 5, 5, 1)[0]
        enemy = env.put_creatures(env.p2, "Enemy", 1, 1, 1)[0]
        stack_creature = env.create_creature(env.p2, "Stack C", 2, 2)
        async def _noop():
            return None

        env.room.stack.append((_noop, stack_creature))

        env.room.flag_dict["bullet_time"] = True
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertNotEqual(env.card_zone(enemy), "battlefield")
        self.assertEqual(env.p1.life, 20)

    async def test_warrior_s_forced_challenge_large_blocker_survives_fight(self):
        """Fight uses a random friendly creature; a big blocker is damaged but not destroyed."""
        card_cls = load_card_class_from_path("pycards/Instant/Warrior_s_Forced_Challenge/model.py", "Warrior_s_Forced_Challenge")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "Ally", 5, 5, 1)
        blocker = env.put_creatures(env.p2, "Blocker", 8, 8, 1)[0]
        before = blocker.state

        async def _noop():
            return None

        env.room.stack.append((_noop, creature_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(blocker), "battlefield")
        self.assertLess(blocker.state[1], before[1])

    async def test_warrior_s_forced_challenge_countered_spell_in_graveyard(self):
        card_cls = load_card_class_from_path("pycards/Instant/Warrior_s_Forced_Challenge/model.py", "Warrior_s_Forced_Challenge")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "Ally", 3, 3, 1)
        stack_creature = creature_cls(env.p2)
        env.p2.battlefield.append(stack_creature)

        async def _noop():
            return None

        env.room.stack.append((_noop, stack_creature))
        env.room.flag_dict["bullet_time"] = True
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(stack_creature), "graveyard")
