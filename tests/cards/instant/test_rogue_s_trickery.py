from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestRogue_s_Trickery(CardTestCaseBase):
    async def test_rogue_s_trickery_returns_countered_spell_copy_to_hand(self):
        card_cls = load_card_class_from_path("pycards/Instant/Rogue_s_Trickery/model.py", "Rogue_s_Trickery")
        target_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)
        target = target_cls(env.p2)

        async def _noop():
            return None

        env.room.stack.append((_noop, target))
        hand_before = len(env.p1.hand)
        env.room.flag_dict["bullet_time"] = True
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)
        self.assertEqual(env.p1.hand[-1].name, target.name)

    async def test_rogue_s_trickery_returns_countered_creature_copy(self):
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        card_cls = load_card_class_from_path("pycards/Instant/Rogue_s_Trickery/model.py", "Rogue_s_Trickery")
        env = self.make_env()
        card = card_cls(env.p1)
        stack_creature = creature_cls(env.p2)
        env.p2.battlefield.append(stack_creature)

        async def _noop():
            return None

        env.room.stack.append((_noop, stack_creature))
        hand_before = len(env.p1.hand)
        env.room.flag_dict["bullet_time"] = True
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)
        self.assertEqual(env.p1.hand[-1].name, "Night Stalker")

    async def test_rogue_s_trickery_controller_life_unchanged_on_spell_counter(self):
        card_cls = load_card_class_from_path("pycards/Instant/Rogue_s_Trickery/model.py", "Rogue_s_Trickery")
        target_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)
        target = target_cls(env.p2)
        async def _noop():
            return None
        env.room.stack.append((_noop, target))
        env.room.flag_dict["bullet_time"] = True
        life = env.p1.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life)
