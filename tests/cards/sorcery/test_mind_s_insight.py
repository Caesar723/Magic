from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestMind_s_Insight(CardTestCaseBase):
    async def test_mind_s_insight_draw_three_discard_two_non_island(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Mind_s_Insight/model.py", "Mind_s_Insight")
        forest_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        swamp_cls = load_card_class_from_path("pycards/land/Swamp/model.py", "Swamp")
        mountain_cls = load_card_class_from_path("pycards/land/Mountain/model.py", "Mountain")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [forest_cls(env.p1), swamp_cls(env.p1), mountain_cls(env.p1)]
        hand_before = len(env.p1.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)
        self.assertEqual(len(env.p1.library), 0)
        self.assertTrue(any(c.name == "Mind's Insight" for c in env.p1.graveyard))

    async def test_mind_s_insight_discards_at_most_two_non_islands(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Mind_s_Insight/model.py", "Mind_s_Insight")
        island_cls = load_card_class_from_path("pycards/land/Island/model.py", "Island")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [island_cls(env.p1), island_cls(env.p1), island_cls(env.p1)]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        island_in_grave = [c for c in env.p1.graveyard if getattr(c, "name", "") == "Island"]
        self.assertLessEqual(len(island_in_grave), 2)

    async def test_mind_s_insight_does_not_touch_opponent_hand(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Mind_s_Insight/model.py", "Mind_s_Insight")
        forest_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        swamp_cls = load_card_class_from_path("pycards/land/Swamp/model.py", "Swamp")
        mountain_cls = load_card_class_from_path("pycards/land/Mountain/model.py", "Mountain")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [forest_cls(env.p1), swamp_cls(env.p1), mountain_cls(env.p1)]
        opp_hand_before = len(env.p2.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.hand), opp_hand_before)
