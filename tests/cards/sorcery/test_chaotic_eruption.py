from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestChaotic_Eruption(CardTestCaseBase):
    async def test_chaotic_eruption_destroys_target_opponent_land(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Chaotic_Eruption/model.py", "Chaotic_Eruption")
        env = self.make_env()
        card = card_cls(env.p1)

        land = env.p2.hand.pop(0)
        env.p2.land_area.append(land)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotIn(land, env.p2.land_area)
        self.assertIn(land, env.p2.graveyard)

    async def test_chaotic_eruption_no_target_land_does_not_crash(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Chaotic_Eruption/model.py", "Chaotic_Eruption")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p2.land_area = []
        result = await env.play_card(card, env.p1)
        self.assertFalse(result[0])

    async def test_chaotic_eruption_only_destroys_one_land(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Chaotic_Eruption/model.py", "Chaotic_Eruption")
        env = self.make_env()
        card = card_cls(env.p1)

        first_land = env.p2.hand.pop(0)
        second_land = env.p2.hand.pop(0)
        env.p2.land_area.extend([first_land, second_land])
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.land_area), 1)
        self.assertEqual(len(env.p2.graveyard), 1)
