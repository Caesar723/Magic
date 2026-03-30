from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestEthereal_Surge(CardTestCaseBase):
    async def test_ethereal_surge_counters_stack_spell_in_bullet_time(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ethereal_Surge/model.py", "Ethereal_Surge")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)
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

    async def test_ethereal_surge_controller_life_unchanged_after_counter(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ethereal_Surge/model.py", "Ethereal_Surge")
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

    async def test_ethereal_surge_cannot_cast_outside_bullet_time(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ethereal_Surge/model.py", "Ethereal_Surge")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)
        stack_creature = creature_cls(env.p2)
        env.p2.battlefield.append(stack_creature)

        async def _noop():
            return None

        env.room.stack.append((_noop, stack_creature))
        env.room.flag_dict["bullet_time"] = False

        result = await env.play_card(card, env.p1)
        self.assertFalse(result[0])
