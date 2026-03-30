from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestWitch_s_Curse_Counter(CardTestCaseBase):
    async def test_witch_s_curse_counter_halves_enemy_creatures(self):
        card_cls = load_card_class_from_path("pycards/Instant/Witch_s_Curse_Counter/model.py", "Witch_s_Curse_Counter")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        enemy = env.put_creatures(env.p2, "Cursed", 4, 4, 1)[0]

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertLessEqual(enemy.state[0], 2)
        self.assertLessEqual(enemy.state[1], 2)

    async def test_witch_s_curse_counter_empty_opponent_battlefield(self):
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        card_cls = load_card_class_from_path("pycards/Instant/Witch_s_Curse_Counter/model.py", "Witch_s_Curse_Counter")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True
        self.assertEqual(len(env.p2.battlefield), 0)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.battlefield), 0)

    async def test_witch_s_curse_counter_controller_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Witch_s_Curse_Counter/model.py", "Witch_s_Curse_Counter")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Cursed", 4, 4, 1)
        async def _noop():
            return None
        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True
        life = env.p1.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life)
