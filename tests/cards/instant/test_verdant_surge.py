from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestVerdant_Surge(CardTestCaseBase):
    async def test_verdant_surge_adds_stats(self):
        card_cls = load_card_class_from_path("pycards/Instant/Verdant_Surge/model.py", "Verdant_Surge")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Buff Me", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertGreaterEqual(creature.state[0], 4)
        self.assertGreaterEqual(creature.state[1], 6)

    async def test_verdant_surge_druid_gains_reach(self):
        card_cls = load_card_class_from_path("pycards/Instant/Verdant_Surge/model.py", "Verdant_Surge")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Druid Ally", 2, 2, 1)[0]
        creature.type_creature = "Druid"
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertTrue(creature.get_flag("reach"))

    async def test_verdant_surge_non_druid_does_not_gain_reach(self):
        card_cls = load_card_class_from_path("pycards/Instant/Verdant_Surge/model.py", "Verdant_Surge")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Elf Warrior", 2, 2, 1)[0]
        creature.type_creature = "Creature - Elf Warrior"
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertGreaterEqual(creature.state[1], 6)
        self.assertFalse(creature.get_flag("reach"))
