from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestBlazeheart_Berserker__(CardTestCaseBase):
    async def test_blazeheart_berserker_attack_gets_power_from_mountains(self):
        card_cls = load_card_class_from_path("pycards/creature/Blazeheart_Berserker__/model.py", "Blazeheart_Berserker__")
        env = self.make_env()
        card = card_cls(env.p1)

        mountain_cls = card.when_start_attcak.__globals__["Mountain"]
        env.p1.land_area.append(mountain_cls(env.p1))
        env.p1.land_area.append(mountain_cls(env.p1))

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        berserker = env.get_battlefield_creature(env.p1, "Blazeheart Berserker")
        before = berserker.state
        await env.trigger(berserker, "when_start_attcak", env.p2, env.p1, env.p2)
        self.assertEqual(berserker.state[0], before[0] + 2)
        self.assertEqual(berserker.state[1], before[1])

    async def test_blazeheart_berserker_no_mountains_no_power_buff_on_attack(self):
        card_cls = load_card_class_from_path("pycards/creature/Blazeheart_Berserker__/model.py", "Blazeheart_Berserker__")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        berserker = env.get_battlefield_creature(env.p1, "Blazeheart Berserker")
        before = tuple(berserker.state)
        await env.trigger(berserker, "when_start_attcak", env.p2, env.p1, env.p2)
        self.assertEqual(tuple(berserker.state), before)

    async def test_blazeheart_berserker_single_mountain_adds_one_power(self):
        card_cls = load_card_class_from_path("pycards/creature/Blazeheart_Berserker__/model.py", "Blazeheart_Berserker__")
        env = self.make_env()
        card = card_cls(env.p1)
        mountain_cls = card.when_start_attcak.__globals__["Mountain"]
        env.p1.land_area.append(mountain_cls(env.p1))

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        berserker = env.get_battlefield_creature(env.p1, "Blazeheart Berserker")
        before_p, before_t = berserker.state[0], berserker.state[1]
        await env.trigger(berserker, "when_start_attcak", env.p2, env.p1, env.p2)
        self.assertEqual(berserker.state[0], before_p + 1)
        self.assertEqual(berserker.state[1], before_t)
