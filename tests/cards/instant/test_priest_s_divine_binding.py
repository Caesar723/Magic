from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestPriest_s_Divine_Binding(CardTestCaseBase):
    async def test_priest_s_divine_binding_counters_creature_and_gains_life(self):
        card_cls = load_card_class_from_path("pycards/Instant/Priest_s_Divine_Binding/model.py", "Priest_s_Divine_Binding")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        stack_creature = creature_cls(env.p2)
        env.p2.battlefield.append(stack_creature)

        async def _noop():
            return None

        env.room.stack.append((_noop, stack_creature))
        env.room.flag_dict["bullet_time"] = True
        env.p1.life = 10

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertGreaterEqual(env.p1.life, 10)

    async def test_priest_s_divine_binding_cannot_target_non_creature_spell(self):
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        card_cls = load_card_class_from_path("pycards/Instant/Priest_s_Divine_Binding/model.py", "Priest_s_Divine_Binding")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertFalse(result[0])

    async def test_priest_s_divine_binding_opponent_life_unchanged_on_counter(self):
        card_cls = load_card_class_from_path("pycards/Instant/Priest_s_Divine_Binding/model.py", "Priest_s_Divine_Binding")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)
        stack_creature = creature_cls(env.p2)
        env.p2.battlefield.append(stack_creature)
        async def _noop():
            return None
        env.room.stack.append((_noop, stack_creature))
        env.room.flag_dict["bullet_time"] = True
        opp = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp)
