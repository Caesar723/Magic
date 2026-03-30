from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestLuminous_Angel(CardTestCaseBase):
    async def test_luminous_angel_keywords_and_upkeep_growth(self):
        card_cls = load_card_class_from_path("pycards/creature/Luminous_Angel/model.py", "Luminous_Angel")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        angel = env.get_battlefield_creature(env.p1, "Luminous Angel")
        self.assert_state(angel, {"flags": {"flying": True, "lifelink": True}, "state": (4, 4)})

        env.p1.life = 20
        await env.trigger(angel, "when_start_turn", env.p1, env.p2)
        self.assertEqual(angel.state, (5, 5))

    async def test_luminous_angel_upkeep_no_growth_below_twenty_life(self):
        card_cls = load_card_class_from_path("pycards/creature/Luminous_Angel/model.py", "Luminous_Angel")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        angel = env.get_battlefield_creature(env.p1, "Luminous Angel")
        env.p1.life = 19
        before = tuple(angel.state)
        await env.trigger(angel, "when_start_turn", env.p1, env.p2)
        self.assertEqual(tuple(angel.state), before)

    async def test_luminous_angel_upkeep_growth_at_exactly_twenty_life(self):
        card_cls = load_card_class_from_path("pycards/creature/Luminous_Angel/model.py", "Luminous_Angel")
        env = self.make_env()
        card = card_cls(env.p1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        angel = env.get_battlefield_creature(env.p1, "Luminous Angel")
        env.p1.life = 20
        await env.trigger(angel, "when_start_turn", env.p1, env.p2)
        self.assertEqual(angel.state, (5, 5))
