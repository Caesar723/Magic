from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestOvergrowth_Surge(CardTestCaseBase):
    async def test_overgrowth_surge_gives_plus_three_plus_three(self):
        card_cls = load_card_class_from_path("pycards/Instant/Overgrowth_Surge/model.py", "Overgrowth_Surge")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Buff Target", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertGreaterEqual(creature.state[0], 5)
        self.assertGreaterEqual(creature.state[1], 5)

    async def test_overgrowth_surge_treefolk_gains_trample(self):
        card_cls = load_card_class_from_path("pycards/Instant/Overgrowth_Surge/model.py", "Overgrowth_Surge")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Ancient Bark", 2, 2, 1)[0]
        creature.type_creature = "Creature - Treefolk"
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertTrue(creature.get_flag("Trample"))

    async def test_overgrowth_surge_non_treefolk_does_not_gain_trample(self):
        card_cls = load_card_class_from_path("pycards/Instant/Overgrowth_Surge/model.py", "Overgrowth_Surge")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Human Scout", 2, 2, 1)[0]
        creature.type_creature = "Creature - Human Scout"
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertGreaterEqual(creature.state[0], 5)
        self.assertFalse(creature.get_flag("Trample"))
