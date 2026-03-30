from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestFleeting_Insight(CardTestCaseBase):
    async def test_fleeting_insight_draw_one_discard_one(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Fleeting_Insight/model.py", "Fleeting_Insight")
        forest_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        swamp_cls = load_card_class_from_path("pycards/land/Swamp/model.py", "Swamp")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [forest_cls(env.p1), swamp_cls(env.p1)]
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before)
        self.assertEqual(len(env.p1.library), 1)
        self.assertTrue(any(c.name == "Fleeting Insight" for c in env.p1.graveyard))

    async def test_fleeting_insight_scripted_discard_targets_specific_card(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Fleeting_Insight/model.py", "Fleeting_Insight")
        forest_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        swamp_cls = load_card_class_from_path("pycards/land/Swamp/model.py", "Swamp")
        env = self.make_env()
        card = card_cls(env.p1)

        to_discard = swamp_cls(env.p1)
        env.p1.library = [forest_cls(env.p1)]
        env.p1.hand = [card, to_discard]
        env.script_selection(env.p1, [to_discard])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertIsNotNone(env.find_card_by_name(env.p1, "Forest", zones=("hand",)))
        self.assertIsNone(env.find_card_by_name(env.p1, "Swamp", zones=("hand",)))

    async def test_fleeting_insight_does_not_change_opponent_library_size(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Fleeting_Insight/model.py", "Fleeting_Insight")
        forest_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        swamp_cls = load_card_class_from_path("pycards/land/Swamp/model.py", "Swamp")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [forest_cls(env.p1), swamp_cls(env.p1)]
        opp_lib_before = len(env.p2.library)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.library), opp_lib_before)
