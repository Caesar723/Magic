from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestEldritch_Rebirth(CardTestCaseBase):
    async def test_eldritch_rebirth_returns_small_creatures_from_graveyard(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Eldritch_Rebirth/model.py", "Eldritch_Rebirth")
        small_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        dead = small_cls(env.p1)
        env.p1.graveyard.append(dead)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertIn(dead, env.p1.battlefield)

    async def test_eldritch_rebirth_skips_high_cmc_creatures(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Eldritch_Rebirth/model.py", "Eldritch_Rebirth")
        big_cls = load_card_class_from_path("pycards/creature/Inferno_Titan/model.py", "Inferno_Titan")
        env = self.make_env()
        card = card_cls(env.p1)
        big = big_cls(env.p1)
        env.p1.graveyard.append(big)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(big), "graveyard")
        self.assertEqual(len(env.p1.battlefield), 0)

    async def test_eldritch_rebirth_does_not_return_opponent_graveyard_creatures(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Eldritch_Rebirth/model.py", "Eldritch_Rebirth")
        small_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        theirs = small_cls(env.p2)
        env.p2.graveyard.append(theirs)
        env.p1.graveyard.clear()

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertIn(theirs, env.p2.graveyard)
        self.assertFalse(env.p1.battlefield)
