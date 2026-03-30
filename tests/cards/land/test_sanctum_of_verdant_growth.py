from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestSanctum_of_Verdant_Growth(CardTestCaseBase):
    async def test_sanctum_of_verdant_growth_plays_to_land_area(self):
        card_cls = load_card_class_from_path("pycards/land/Sanctum_of_Verdant_Growth/model.py", "Sanctum_of_Verdant_Growth")
        env = self.make_env()
        card = card_cls(env.p1)

        lands_before = len(env.p1.land_area)
        g_before = env.p1.mana["G"]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.mana["G"], g_before + 1)
        self.assertEqual(len(env.p1.land_area), lands_before + 1)
        self.assertEqual(env.card_zone(card), "land_area")

    async def test_sanctum_of_verdant_growth_when_clicked_generates_expected_mana(self):
        card_cls = load_card_class_from_path("pycards/land/Sanctum_of_Verdant_Growth/model.py", "Sanctum_of_Verdant_Growth")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_on_battlefield(card, env.p1)
        env.p1.action_store.start_record()
        env.p1.remove_card(card, "battlefield")
        env.p1.land_area.append(card)
        env.p1.action_store.end_record()

        mana_before = dict(env.p1.mana)
        expected = card.generate_mana()
        result = await env.trigger(card, "when_clicked", env.p1, env.p2)

        self.assertTrue(result)
        self.assertTrue(card.get_flag("tap"))
        for key, value in expected.items():
            self.assertEqual(env.p1.mana[key], mana_before[key] + value)

    async def test_sanctum_of_verdant_growth_second_play_adds_another_land(self):
        card_cls = load_card_class_from_path("pycards/land/Sanctum_of_Verdant_Growth/model.py", "Sanctum_of_Verdant_Growth")
        env = self.make_env()
        l1, l2 = card_cls(env.p1), card_cls(env.p1)
        await env.play_card(l1, env.p1)
        await env.resolve_stack()
        lands_mid = len(env.p1.land_area)
        await env.play_card(l2, env.p1)
        await env.resolve_stack()
        self.assertEqual(len(env.p1.land_area), lands_mid + 1)

    async def test_sanctum_of_verdant_growth_when_clicked_while_tapped_does_nothing(self):
        card_cls = load_card_class_from_path("pycards/land/Sanctum_of_Verdant_Growth/model.py", "Sanctum_of_Verdant_Growth")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_on_battlefield(card, env.p1)
        env.p1.action_store.start_record()
        env.p1.remove_card(card, "battlefield")
        env.p1.land_area.append(card)
        env.p1.action_store.end_record()
        await env.trigger(card, "when_clicked", env.p1, env.p2)
        mana_after_first = dict(env.p1.mana)
        second = await env.trigger(card, "when_clicked", env.p1, env.p2)
        self.assertFalse(second)
        self.assertEqual(dict(env.p1.mana), mana_after_first)
