from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestPious_Courser(CardTestCaseBase):
    async def test_pious_courser_etb_gains_two_life(self):
        card_cls = load_card_class_from_path("pycards/creature/Pious_Courser/model.py", "Pious_Courser")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.life = 15

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, 17)
        courser = env.get_battlefield_creature(env.p1, "Pious Courser")
        self.assert_state(courser, {"zone": "battlefield", "state": (2, 2)})

    async def test_pious_courser_does_not_change_opponent_life(self):
        card_cls = load_card_class_from_path("pycards/creature/Pious_Courser/model.py", "Pious_Courser")
        env = self.make_env()
        card = card_cls(env.p1)

        opp_before = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_before)

    async def test_pious_courser_increments_controller_battlefield_by_one(self):
        card_cls = load_card_class_from_path("pycards/creature/Pious_Courser/model.py", "Pious_Courser")
        env = self.make_env()
        card = card_cls(env.p1)
        before = len(env.p1.battlefield)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), before + 1)
        self.assertIsNotNone(env.find_card_by_name(env.p1, "Pious Courser", zones=("battlefield",)))
