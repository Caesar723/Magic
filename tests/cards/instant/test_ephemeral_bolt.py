from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestEphemeral_Bolt(CardTestCaseBase):
    async def test_ephemeral_bolt_deals_three_to_single_target(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ephemeral_Bolt/model.py", "Ephemeral_Bolt")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Bolt Target", 2, 4, 1)[0]

        async def _pick_one(player=None, opponent=None, selection_random=False):
            return [target]

        card.selection_step = _pick_one
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(target.state[1], 1)

    async def test_ephemeral_bolt_can_hit_two_targets_in_flashback_mode(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ephemeral_Bolt/model.py", "Ephemeral_Bolt")
        env = self.make_env()
        card = card_cls(env.p1)

        t1 = env.put_creatures(env.p2, "Target One", 2, 4, 1)[0]
        t2 = env.put_creatures(env.p2, "Target Two", 2, 4, 1)[0]

        async def _pick_two(player=None, opponent=None, selection_random=False):
            return [t1, t2]

        card.selection_step = _pick_two
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(t1.state[1], 1)
        self.assertEqual(t2.state[1], 1)

    async def test_ephemeral_bolt_can_target_opponent_player(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ephemeral_Bolt/model.py", "Ephemeral_Bolt")
        env = self.make_env()
        card = card_cls(env.p1)
        life_before = env.p2.life

        async def _pick_oppo(player=None, opponent=None, selection_random=False):
            return [opponent]

        card.selection_step = _pick_oppo
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, life_before - 3)
