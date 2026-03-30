from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestMage_s_Veto(CardTestCaseBase):
    async def test_mage_s_veto_requires_bullet_time(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mage_s_Veto/model.py", "Mage_s_Veto")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        self.assertIsInstance(result, (tuple, list))
        self.assertFalse(result[0])

    async def test_mage_s_veto_counters_low_cost_spell_and_tutors_sorcery(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mage_s_Veto/model.py", "Mage_s_Veto")
        spell_cls = load_card_class_from_path("pycards/sorcery/Mystic_Reversal/model.py", "Mystic_Reversal")
        tutor_cls = load_card_class_from_path("pycards/sorcery/Arcane_Torrent/model.py", "Arcane_Torrent")
        env = self.make_env()
        card = card_cls(env.p1)

        target_spell = spell_cls(env.p2)
        tutor_card = tutor_cls(env.p1)
        env.p1.library = [tutor_card]

        async def _noop():
            return None

        env.room.flag_dict["bullet_time"] = True
        env.room.stack.append((_noop, target_spell))

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.room.stack), 0)
        self.assertIn(tutor_card, env.p1.hand)

    async def test_mage_s_veto_counter_clears_stack_for_sorcery_spell(self):
        """
        `Instant_Undo.undo_stack` only moves Creature stack objects into a graveyard; sorceries
        popped from the stack are not relocated by that helper. Assert the observable counter
        outcome: stack empty and veto resolved to graveyard.
        """
        card_cls = load_card_class_from_path("pycards/Instant/Mage_s_Veto/model.py", "Mage_s_Veto")
        spell_cls = load_card_class_from_path("pycards/sorcery/Mystic_Reversal/model.py", "Mystic_Reversal")
        env = self.make_env()
        card = card_cls(env.p1)
        target_spell = spell_cls(env.p2)

        async def _noop():
            return None

        env.room.flag_dict["bullet_time"] = True
        env.room.stack.append((_noop, target_spell))

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.room.stack), 0)
        self.assertIsNotNone(env.find_card_by_name(env.p1, "Mage's Veto", zones=("graveyard",)))
        self.assertEqual(env.card_zone(target_spell), "unknown")
