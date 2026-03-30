from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestWarlock_s_Dark_Pact(CardTestCaseBase):
    async def test_warlock_s_dark_pact_deals_life_loss_equal_to_cost(self):
        card_cls = load_card_class_from_path("pycards/Instant/Warlock_s_Dark_Pact/model.py", "Warlock_s_Dark_Pact")
        target_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        target_spell = target_cls(env.p2)
        async def _noop():
            return None

        env.room.stack.append((_noop, target_spell))
        env.p2.life = 10
        env.room.flag_dict["bullet_time"] = True
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, 7)

    async def test_warlock_s_dark_pact_creature_spell_uses_creature_cost(self):
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        card_cls = load_card_class_from_path("pycards/Instant/Warlock_s_Dark_Pact/model.py", "Warlock_s_Dark_Pact")
        env = self.make_env()
        card = card_cls(env.p1)
        stack_creature = creature_cls(env.p2)
        env.p2.battlefield.append(stack_creature)

        async def _noop():
            return None

        env.room.stack.append((_noop, stack_creature))
        env.p2.life = 20
        life_before = env.p2.life
        env.room.flag_dict["bullet_time"] = True
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, life_before - sum(stack_creature.cost.values()))

    async def test_warlock_s_dark_pact_controller_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Warlock_s_Dark_Pact/model.py", "Warlock_s_Dark_Pact")
        target_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)
        target_spell = target_cls(env.p2)
        async def _noop():
            return None
        env.room.stack.append((_noop, target_spell))
        env.room.flag_dict["bullet_time"] = True
        life = env.p1.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life)
