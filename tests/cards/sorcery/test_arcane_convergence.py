from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestArcane_Convergence(CardTestCaseBase):
    async def test_arcane_convergence_untaps_all_your_lands(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Arcane_Convergence/model.py", "Arcane_Convergence")
        env = self.make_env()
        card = card_cls(env.p1)

        land1 = env.p1.hand.pop(0)
        land2 = env.p1.hand.pop(0)
        env.p1.land_area.extend([land1, land2])
        land1.flag_dict["tap"] = True
        land2.flag_dict["tap"] = True

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertFalse(land1.get_flag("tap"))
        self.assertFalse(land2.get_flag("tap"))
        self.assertEqual(env.card_zone(card), "graveyard")

    async def test_arcane_convergence_no_tapped_lands_still_resolves(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Arcane_Convergence/model.py", "Arcane_Convergence")
        env = self.make_env()
        card = card_cls(env.p1)

        land1 = env.p1.hand.pop(0)
        land2 = env.p1.hand.pop(0)
        env.p1.land_area.extend([land1, land2])
        mana_before = dict(env.p1.mana)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertFalse(land1.get_flag("tap"))
        self.assertFalse(land2.get_flag("tap"))
        self.assertEqual(env.p1.mana, mana_before)
        self.assertEqual(env.card_zone(card), "graveyard")

    async def test_arcane_convergence_does_not_untap_opponent_lands(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Arcane_Convergence/model.py", "Arcane_Convergence")
        env = self.make_env()
        card = card_cls(env.p1)
        opp_land = env.p2.hand.pop(0)
        env.p2.land_area.append(opp_land)
        opp_land.flag_dict["tap"] = True

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertTrue(opp_land.get_flag("tap"))
        self.assertEqual(env.card_zone(card), "graveyard")
