from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestSunlit_Priestess(CardTestCaseBase):
    async def test_sunlit_priestess_etb_gain_three_life(self):
        card_cls = load_card_class_from_path("pycards/creature/Sunlit_Priestess/model.py", "Sunlit_Priestess")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.life = 10

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        priestess = env.get_battlefield_creature(env.p1, "Sunlit Priestess")
        self.assert_state(priestess, {"zone": "battlefield", "state": (2, 2)})
        self.assertEqual(env.p1.life, 13)

    async def test_sunlit_priestess_does_not_change_opponent_life(self):
        card_cls = load_card_class_from_path("pycards/creature/Sunlit_Priestess/model.py", "Sunlit_Priestess")
        env = self.make_env()
        card = card_cls(env.p1)

        opp_before = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_before)

    async def test_sunlit_priestess_etb_gains_three_even_from_low_starting_life(self):
        card_cls = load_card_class_from_path("pycards/creature/Sunlit_Priestess/model.py", "Sunlit_Priestess")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.life = 1

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, 4)
