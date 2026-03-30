from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestRanger_s_Sniping_Shot(CardTestCaseBase):
    async def test_ranger_s_sniping_shot_counters_and_hits_controller(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ranger_s_Sniping_Shot/model.py", "Ranger_s_Sniping_Shot")
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
        self.assertLess(env.p2.life, 10)
        self.assertEqual(env.p1.life, 20)

    async def test_ranger_s_sniping_shot_instant_spell_no_creature_damage(self):
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        card_cls = load_card_class_from_path("pycards/Instant/Ranger_s_Sniping_Shot/model.py", "Ranger_s_Sniping_Shot")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True
        env.p2.life = 15
        life_before = env.p2.life

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, life_before)

    async def test_ranger_s_sniping_shot_creature_counter_puts_stack_spell_in_graveyard(self):
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        card_cls = load_card_class_from_path("pycards/Instant/Ranger_s_Sniping_Shot/model.py", "Ranger_s_Sniping_Shot")
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
        self.assertEqual(env.card_zone(stack_creature), "graveyard")
