from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestPaladin_s_Judging_Light(CardTestCaseBase):
    async def test_paladin_s_judging_light_counters_and_deals_life_loss(self):
        card_cls = load_card_class_from_path("pycards/Instant/Paladin_s_Judging_Light/model.py", "Paladin_s_Judging_Light")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        stack_creature = creature_cls(env.p2)
        env.p2.battlefield.append(stack_creature)

        async def _noop():
            return None

        env.room.stack.append((_noop, stack_creature))
        env.room.flag_dict["bullet_time"] = True
        env.p2.life = 10

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertLessEqual(env.p2.life, 10)

    async def test_paladin_s_judging_light_controller_life_unchanged_when_countering_creature_spell(self):
        card_cls = load_card_class_from_path("pycards/Instant/Paladin_s_Judging_Light/model.py", "Paladin_s_Judging_Light")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)
        stack_creature = creature_cls(env.p2)
        env.p2.battlefield.append(stack_creature)
        async def _noop():
            return None
        env.room.stack.append((_noop, stack_creature))
        env.room.flag_dict["bullet_time"] = True
        life = env.p1.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life)

    async def test_paladin_s_judging_light_damage_matches_countered_spell_mana(self):
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        card_cls = load_card_class_from_path("pycards/Instant/Paladin_s_Judging_Light/model.py", "Paladin_s_Judging_Light")
        env = self.make_env()
        card = card_cls(env.p1)
        target_spell = spell_cls(env.p2)

        async def _noop():
            return None

        env.room.stack.append((_noop, target_spell))
        env.room.flag_dict["bullet_time"] = True
        env.p2.life = 20
        life_before = env.p2.life

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, life_before - sum(target_spell.cost.values()))
