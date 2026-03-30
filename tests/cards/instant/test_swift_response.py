from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestSwift_Response(CardTestCaseBase):
    async def test_swift_response_destroys_power_two_or_less(self):
        card_cls = load_card_class_from_path("pycards/Instant/Swift_Response/model.py", "Swift_Response")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Small Target", 2, 2, 1)[0]
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "graveyard")
        self.assertEqual(env.p1.life, 20)

    async def test_swift_response_does_not_destroy_power_above_two(self):
        card_cls = load_card_class_from_path("pycards/Instant/Swift_Response/model.py", "Swift_Response")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Big Target", 3, 3, 1)[0]
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "battlefield")

    async def test_swift_response_destroys_exactly_power_two(self):
        card_cls = load_card_class_from_path("pycards/Instant/Swift_Response/model.py", "Swift_Response")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Two Power", 2, 4, 1)[0]
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "graveyard")
