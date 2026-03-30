from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestNight_Stalker__(CardTestCaseBase):
    async def test_night_stalker_has_menace_flag(self):
        card_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        stalker = env.get_battlefield_creature(env.p1, "Night Stalker")
        self.assert_state(stalker, {"zone": "battlefield", "state": (2, 1), "flags": {"Menace": True}})

    async def test_night_stalker_does_not_have_unrelated_keywords(self):
        card_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        stalker = env.get_battlefield_creature(env.p1, "Night Stalker")
        self.assertFalse(stalker.get_flag("flying"))
        self.assertFalse(stalker.get_flag("lifelink"))

    async def test_night_stalker_etb_does_not_change_opponent_life(self):
        card_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)
        opp_before = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_before)
