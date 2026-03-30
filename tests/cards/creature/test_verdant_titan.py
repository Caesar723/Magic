from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestVerdant_Titan(CardTestCaseBase):
    async def test_verdant_titan_etb_and_attack_each_put_land_tapped(self):
        card_cls = load_card_class_from_path("pycards/creature/Verdant_Titan/model.py", "Verdant_Titan")
        env = self.make_env()
        card = card_cls(env.p1)

        forest_cls = card.put_land.__globals__["Forest"]
        env.p1.library = [forest_cls(env.p1), forest_cls(env.p1)]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        titan = env.get_battlefield_creature(env.p1, "Verdant Titan")
        self.assert_state(titan, {"flags": {"Trample": True, "Vigilance": True}, "state": (5, 5)})
        self.assertEqual(len(env.p1.land_area), 1)
        self.assertTrue(env.p1.land_area[0].get_flag("tap"))

        await env.trigger(titan, "when_start_attcak", env.p2, env.p1, env.p2)
        self.assertEqual(len(env.p1.land_area), 2)
        self.assertTrue(env.p1.land_area[1].get_flag("tap"))

    async def test_verdant_titan_empty_library_etb_no_extra_land(self):
        card_cls = load_card_class_from_path("pycards/creature/Verdant_Titan/model.py", "Verdant_Titan")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library.clear()
        lands_before = len(env.p1.land_area)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), lands_before)

    async def test_verdant_titan_etb_does_not_put_lands_under_opponent_control(self):
        card_cls = load_card_class_from_path("pycards/creature/Verdant_Titan/model.py", "Verdant_Titan")
        env = self.make_env()
        card = card_cls(env.p1)
        forest_cls = card.put_land.__globals__["Forest"]
        env.p1.library = [forest_cls(env.p1)]
        opp_lands_before = len(env.p2.land_area)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.land_area), opp_lands_before)
