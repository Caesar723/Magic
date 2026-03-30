from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestDreamweaver_Archivist(CardTestCaseBase):
    async def test_dreamweaver_archivist_choose_draw_then_discard_keeps_hand_size(self):
        card_cls = load_card_class_from_path("pycards/creature/Dreamweaver_Archivist/model.py", "Dreamweaver_Archivist")
        env = self.make_env()
        card = card_cls(env.p1)

        hand_before = len(env.p1.hand)
        env.script_selection(env.p1, [0])  # choose "draw a card and discard a card"

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        archivist = env.get_battlefield_creature(env.p1, "Dreamweaver Archivist")
        self.assert_state(archivist, {"zone": "battlefield", "state": (2, 2)})
        # play consumes one card from hand; ETB draw+discard net 0
        self.assertEqual(len(env.p1.hand), hand_before - 1)

    async def test_dreamweaver_archivist_draw_with_empty_library_still_resolves(self):
        """Draw branch with empty library: ETB still completes and creature enters."""
        card_cls = load_card_class_from_path("pycards/creature/Dreamweaver_Archivist/model.py", "Dreamweaver_Archivist")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library.clear()
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.library), 0)
        env.get_battlefield_creature(env.p1, "Dreamweaver Archivist")

    async def test_dreamweaver_archivist_do_nothing_option_leaves_hand_size_stable(self):
        card_cls = load_card_class_from_path("pycards/creature/Dreamweaver_Archivist/model.py", "Dreamweaver_Archivist")
        env = self.make_env()
        card = card_cls(env.p1)

        opening_hand = len(env.p1.hand)
        lib_before = len(env.p1.library)
        env.script_selection(env.p1, [1])  # "Do nothing" selection card (selection_index 2)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        archivist = env.get_battlefield_creature(env.p1, "Dreamweaver Archivist")
        self.assert_state(archivist, {"zone": "battlefield"})
        # play_card adds then resolves to battlefield; ETB branch skipped → same count as before cast
        self.assertEqual(len(env.p1.hand), opening_hand)
        self.assertEqual(len(env.p1.library), lib_before)
