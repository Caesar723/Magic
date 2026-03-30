from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestWizard_s_Time_Warp(CardTestCaseBase):
    async def test_wizard_s_time_warp_counters_and_forces_discard(self):
        card_cls = load_card_class_from_path("pycards/Instant/Wizard_s_Time_Warp/model.py", "Wizard_s_Time_Warp")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True
        env.p2.hand.append(spell_cls(env.p2))
        hand_before = len(env.p2.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.hand), hand_before - 1)

    async def test_wizard_s_time_warp_skips_discard_when_opponent_hand_empty(self):
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        card_cls = load_card_class_from_path("pycards/Instant/Wizard_s_Time_Warp/model.py", "Wizard_s_Time_Warp")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True
        env.p2.hand.clear()
        self.assertEqual(len(env.p2.hand), 0)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.hand), 0)

    async def test_wizard_s_time_warp_controller_life_unchanged(self):
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        card_cls = load_card_class_from_path("pycards/Instant/Wizard_s_Time_Warp/model.py", "Wizard_s_Time_Warp")
        env = self.make_env()
        card = card_cls(env.p1)
        async def _noop():
            return None
        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True
        env.p2.hand.append(spell_cls(env.p2))
        life = env.p1.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life)
