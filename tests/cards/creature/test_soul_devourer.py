from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestSoul_Devourer(CardTestCaseBase):
    async def test_soul_devourer_gains_stat_for_dead_creature_power(self):
        card_cls = load_card_class_from_path("pycards/creature/Soul_Devourer/model.py", "Soul_Devourer")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_on_battlefield(card, env.p1)
        before = card.state
        dead = env.create_creature(env.p2, "Dead 3 Power", 3, 1)
        await env.trigger(card, "when_a_creature_die", dead, env.p1, env.p2)

        self.assertEqual(card.state, (before[0] + 3, before[1] + 3))

    async def test_soul_devourer_no_growth_when_not_on_battlefield(self):
        card_cls = load_card_class_from_path("pycards/creature/Soul_Devourer/model.py", "Soul_Devourer")
        env = self.make_env()
        card = card_cls(env.p1)

        before = card.state
        dead = env.create_creature(env.p2, "Dead 3 Power", 3, 1)
        await env.trigger(card, "when_a_creature_die", dead, env.p1, env.p2)

        self.assertEqual(card.state, before)

    async def test_soul_devourer_zero_power_death_adds_nothing(self):
        card_cls = load_card_class_from_path("pycards/creature/Soul_Devourer/model.py", "Soul_Devourer")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_on_battlefield(card, env.p1)
        before = card.state
        dead = env.create_creature(env.p2, "Zero Power", 0, 1)
        await env.trigger(card, "when_a_creature_die", dead, env.p1, env.p2)
        self.assertEqual(card.state, before)
