from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestDivine_Intervention(CardTestCaseBase):
    async def test_divine_intervention_exiles_all_nonland_permanents(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Divine_Intervention/model.py", "Divine_Intervention")
        env = self.make_env()
        card = card_cls(env.p1)

        c1 = env.put_creatures(env.p1, "Self C", 2, 2, 1)[0]
        c2 = env.put_creatures(env.p2, "Enemy C", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotEqual(env.card_zone(c1), "battlefield")
        self.assertNotEqual(env.card_zone(c2), "battlefield")

    async def test_divine_intervention_leaves_lands_untouched(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Divine_Intervention/model.py", "Divine_Intervention")
        env = self.make_env()
        card = card_cls(env.p1)

        land_1 = env.p1.hand.pop(0)
        land_2 = env.p2.hand.pop(0)
        env.p1.land_area.append(land_1)
        env.p2.land_area.append(land_2)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertIn(land_1, env.p1.land_area)
        self.assertIn(land_2, env.p2.land_area)

    async def test_divine_intervention_empty_battlefields_exiles_nothing_but_resolves(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Divine_Intervention/model.py", "Divine_Intervention")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.battlefield.clear()
        env.p2.battlefield.clear()

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertFalse(env.p1.battlefield)
        self.assertFalse(env.p2.battlefield)
