from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestAlchemist_s_Chaotic_Blend(CardTestCaseBase):
    async def test_alchemist_s_chaotic_blend_casts_random_spell_from_library(self):
        card_cls = load_card_class_from_path("pycards/Instant/Alchemist_s_Chaotic_Blend/model.py", "Alchemist_s_Chaotic_Blend")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.p1.library = [spell_cls(env.p1)]
        lib_before = len(env.p1.library)
        env.room.flag_dict["bullet_time"] = True
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.library), lib_before - 1)

    async def test_alchemist_s_chaotic_blend_no_library_spell_after_counter(self):
        """After undo, an empty library skips the random cast branch."""
        card_cls = load_card_class_from_path("pycards/Instant/Alchemist_s_Chaotic_Blend/model.py", "Alchemist_s_Chaotic_Blend")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.p1.library = []
        env.room.flag_dict["bullet_time"] = True
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.library), 0)

    async def test_alchemist_s_chaotic_blend_does_not_change_opponent_life(self):
        card_cls = load_card_class_from_path("pycards/Instant/Alchemist_s_Chaotic_Blend/model.py", "Alchemist_s_Chaotic_Blend")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.p1.library = [spell_cls(env.p1)]
        env.room.flag_dict["bullet_time"] = True
        opp_life = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_life)
