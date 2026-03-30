from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestDruid_s_Natural_Fury(CardTestCaseBase):
    async def test_druid_s_natural_fury_counters_and_makes_beast_token(self):
        card_cls = load_card_class_from_path("pycards/Instant/Druid_s_Natural_Fury/model.py", "Druid_s_Natural_Fury")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertTrue(any(c.name == "Beast" for c in env.p1.battlefield))

    async def test_druid_s_natural_fury_token_power_matches_countered_spell_cost(self):
        card_cls = load_card_class_from_path("pycards/Instant/Druid_s_Natural_Fury/model.py", "Druid_s_Natural_Fury")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        stack_spell = spell_cls(env.p2)
        expected = sum(stack_spell.cost.values())

        async def _noop():
            return None

        env.room.stack.append((_noop, stack_spell))
        env.room.flag_dict["bullet_time"] = True

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        beast = next(c for c in env.p1.battlefield if c.name == "Beast")
        self.assertEqual(beast.state, (expected, expected))

    async def test_druid_s_natural_fury_controller_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Druid_s_Natural_Fury/model.py", "Druid_s_Natural_Fury")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)
        async def _noop():
            return None
        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True
        life = env.p1.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life)
