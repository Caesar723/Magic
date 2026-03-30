from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestArcane_Reflection(CardTestCaseBase):
    async def test_arcane_reflection_returns_spell_from_graveyard(self):
        card_cls = load_card_class_from_path("pycards/Instant/Arcane_Reflection/model.py", "Arcane_Reflection")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        dead_spell = spell_cls(env.p1)
        env.p1.graveyard.append(dead_spell)
        hand_before = len(env.p1.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        # play_card briefly adds the instant to hand; after cast + bounce, net +1 card vs pre-cast hand.
        self.assertEqual(len(env.p1.hand), hand_before + 1)
        self.assertNotIn(dead_spell, env.p1.graveyard)
        self.assertIn(dead_spell, env.p1.hand)
        self.assertIn(card, env.p1.graveyard)

    async def test_arcane_reflection_no_legal_graveyard_target_resolves_to_graveyard(self):
        """With no other instant/sorcery in graveyard, ability is a no-op; the spell still resolves to graveyard."""
        card_cls = load_card_class_from_path("pycards/Instant/Arcane_Reflection/model.py", "Arcane_Reflection")
        env = self.make_env()
        card = card_cls(env.p1)
        self.assertFalse(env.p1.graveyard)
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before)
        self.assertNotIn(card, env.p1.hand)
        self.assertIn(card, env.p1.graveyard)

    async def test_arcane_reflection_graveyard_only_creature_no_bounce_spell_still_in_graveyard(self):
        """Non-spell cards in graveyard do not count; Arcane Reflection still resolves normally."""
        card_cls = load_card_class_from_path("pycards/Instant/Arcane_Reflection/model.py", "Arcane_Reflection")
        creature_cls = load_card_class_from_path("pycards/creature/Elite_Squire/model.py", "Elite_Squire")
        env = self.make_env()
        dead_creature = creature_cls(env.p1)
        env.p1.graveyard.append(dead_creature)
        card = card_cls(env.p1)
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before)
        self.assertIn(dead_creature, env.p1.graveyard)
        self.assertIn(card, env.p1.graveyard)
