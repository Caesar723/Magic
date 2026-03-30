from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestAstral_Resurgence(CardTestCaseBase):
    async def test_astral_resurgence_reanimates_and_grants_lifelink(self):
        card_cls = load_card_class_from_path("pycards/Instant/Astral_Resurgence/model.py", "Astral_Resurgence")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.graveyard.append(creature_cls(env.p1))
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        revived = env.find_card_by_name(env.p1, "Night Stalker", zones=("battlefield",))
        self.assertIsNotNone(revived)
        self.assert_state(revived, {"buffs_contains": ["KeyBuff"]})
        lifelink_buffs = [b for b in revived.buffs if type(b).__name__ == "KeyBuff" and getattr(b, "key_name", "") == "lifelink"]
        self.assertEqual(len(lifelink_buffs), 1)

    async def test_astral_resurgence_empty_graveyard_does_not_put_creature_on_field(self):
        card_cls = load_card_class_from_path("pycards/Instant/Astral_Resurgence/model.py", "Astral_Resurgence")
        env = self.make_env()
        card = card_cls(env.p1)
        before_bf = len(env.p1.battlefield)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), before_bf)

    async def test_astral_resurgence_non_creature_in_graveyard_is_ignored(self):
        card_cls = load_card_class_from_path("pycards/Instant/Astral_Resurgence/model.py", "Astral_Resurgence")
        forest_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.graveyard.append(forest_cls(env.p1))
        before_bf = len(env.p1.battlefield)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), before_bf)
        self.assertFalse(any(c.name == "Forest" for c in env.p1.battlefield))
