from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestHarvest_Blessing(CardTestCaseBase):
    async def test_harvest_blessing_fetches_land_and_buffs_creature(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Harvest_Blessing/model.py", "Harvest_Blessing")
        forest_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p1, "Buff Target", 2, 2, 1)[0]
        env.p1.library = [forest_cls(env.p1)]
        before = target.state

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), 1)
        self.assertTrue(env.p1.land_area[0].get_flag("tap"))
        self.assertEqual(target.state, (before[0] + 1, before[1] + 1))

    async def test_harvest_blessing_without_creature_only_fetches_land(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Harvest_Blessing/model.py", "Harvest_Blessing")
        forest_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [forest_cls(env.p1)]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), 1)
        self.assertTrue(env.p1.land_area[0].get_flag("tap"))

    async def test_harvest_blessing_does_not_fetch_into_opponent_lands(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Harvest_Blessing/model.py", "Harvest_Blessing")
        forest_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [forest_cls(env.p1)]
        opp_lands_before = len(env.p2.land_area)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.land_area), opp_lands_before)
