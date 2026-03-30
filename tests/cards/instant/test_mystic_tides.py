from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestMystic_Tides(CardTestCaseBase):
    async def test_mystic_tides_counters_creature_spell_when_unpaid(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Tides/model.py", "Mystic_Tides")
        env = self.make_env()
        card = card_cls(env.p1)

        stack_creature = env.put_creatures(env.p2, "Stack C", 3, 3, 1)[0]

        async def _noop():
            return None

        env.room.stack.append((_noop, stack_creature))
        env.p2.mana = {"colorless": 0, "U": 0, "W": 0, "B": 0, "R": 0, "G": 0}
        env.room.flag_dict["bullet_time"] = True

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(stack_creature), "graveyard")

    async def test_mystic_tides_opponent_pays_two_creature_not_countered(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Tides/model.py", "Mystic_Tides")
        env = self.make_env()
        card = card_cls(env.p1)
        stack_creature = env.put_creatures(env.p2, "Stack C", 3, 3, 1)[0]
        async def _noop():
            return None
        env.room.stack.append((_noop, stack_creature))
        env.p2.mana = {"colorless": 2, "U": 0, "W": 0, "B": 0, "R": 0, "G": 0}
        env.room.flag_dict["bullet_time"] = True
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(stack_creature), "battlefield")

    async def test_mystic_tides_counter_branch_does_not_change_caster_life(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Tides/model.py", "Mystic_Tides")
        env = self.make_env()
        card = card_cls(env.p1)
        stack_creature = env.put_creatures(env.p2, "Stack C", 3, 3, 1)[0]

        async def _noop():
            return None

        env.room.stack.append((_noop, stack_creature))
        env.p2.mana = {"colorless": 0, "U": 0, "W": 0, "B": 0, "R": 0, "G": 0}
        env.room.flag_dict["bullet_time"] = True
        life_before = env.p1.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life_before)
