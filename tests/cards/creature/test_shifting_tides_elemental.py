from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestShifting_Tides_Elemental(CardTestCaseBase):
    async def test_shifting_tides_elemental_bounces_selected_land_to_new_card(self):
        card_cls = load_card_class_from_path("pycards/creature/Shifting_Tides_Elemental/model.py", "Shifting_Tides_Elemental")
        land_cls = load_card_class_from_path("pycards/land/Mountain/model.py", "Mountain")
        env = self.make_env()
        card = card_cls(env.p1)

        opp_land = land_cls(env.p2)
        env.p2.action_store.start_record()
        env.p2.append_card(opp_land, "land_area")
        env.p2.action_store.end_record()
        hand_before = len(env.p2.hand)

        env.script_selection(env.p1, [0])
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        elemental = env.get_battlefield_creature(env.p1, "Shifting Tides Elemental")
        self.assert_state(elemental, {"zone": "battlefield", "state": (2, 3)})
        self.assertEqual(len(env.p2.land_area), 0)
        self.assertEqual(len(env.p2.hand), hand_before + 1)
        self.assertTrue(any(c.name == "Mountain" for c in env.p2.hand))
        self.assertIsNot(env.p2.hand[-1], opp_land)
        self.assertEqual(env.p1.life, 20)

    async def test_shifting_tides_elemental_can_bounce_own_land(self):
        card_cls = load_card_class_from_path("pycards/creature/Shifting_Tides_Elemental/model.py", "Shifting_Tides_Elemental")
        land_cls = load_card_class_from_path("pycards/land/Island/model.py", "Island")
        env = self.make_env()
        card = card_cls(env.p1)

        own_land = land_cls(env.p1)
        env.p1.land_area.append(own_land)
        hand_before = len(env.p1.hand)

        env.script_selection(env.p1, [own_land])
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), 0)
        self.assertGreaterEqual(len(env.p1.hand), hand_before)
        self.assertIsNotNone(env.find_card_by_name(env.p1, "Island", zones=("hand",)))

    async def test_shifting_tides_elemental_bouncing_only_opp_land_leaves_controller_land_area_empty(self):
        """With no own lands, ETB target list is only opponent lands; bounce does not create p1 lands."""
        card_cls = load_card_class_from_path("pycards/creature/Shifting_Tides_Elemental/model.py", "Shifting_Tides_Elemental")
        land_cls = load_card_class_from_path("pycards/land/Mountain/model.py", "Mountain")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.land_area.clear()
        opp_land = land_cls(env.p2)
        env.p2.land_area.append(opp_land)
        p2_hand_before = len(env.p2.hand)

        env.script_selection(env.p1, [0])
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), 0)
        self.assertGreater(len(env.p2.hand), p2_hand_before)
        self.assertEqual(env.p1.life, 20)
