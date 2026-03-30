from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestChronostrider(CardTestCaseBase):
    async def test_chronostrider_has_flash_haste_and_grants_extra_turn_counter(self):
        card_cls = load_card_class_from_path("pycards/creature/Chronostrider/model.py", "Chronostrider")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        chrono = env.get_battlefield_creature(env.p1, "Chronostrider")
        self.assert_state(chrono, {
            "zone": "battlefield",
            "state": (2, 4),
            "flags": {"haste": True, "Flash": True},
        })
        self.assert_state(env.p1, {"counters": {"extra_turn": 1}})

    async def test_second_chronostrider_stacks_extra_turn_counter(self):
        card_cls = load_card_class_from_path("pycards/creature/Chronostrider/model.py", "Chronostrider")
        env = self.make_env()

        first = card_cls(env.p1)
        result1 = await env.play_card(first, env.p1)
        await env.resolve_stack()
        self.assertTrue(result1[0])

        second = card_cls(env.p1)
        result2 = await env.play_card(second, env.p1)
        await env.resolve_stack()
        self.assertTrue(result2[0])

        self.assert_state(env.p1, {"counters": {"extra_turn": 2}})

    async def test_chronostrider_does_not_increment_opponent_extra_turn_counter(self):
        card_cls = load_card_class_from_path("pycards/creature/Chronostrider/model.py", "Chronostrider")
        env = self.make_env()
        card = card_cls(env.p1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.counter_dict.get("extra_turn", 0), 0)
