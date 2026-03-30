from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestShadow_Snare(CardTestCaseBase):
    async def test_shadow_snare_applies_minus_three_minus_three(self):
        card_cls = load_card_class_from_path("pycards/Instant/Shadow_Snare/model.py", "Shadow_Snare")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Victim", 5, 5, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(target, {"buffs_contains": ["StateBuff"]})
        self.assertEqual(target.state[0], 2)
        self.assertEqual(target.state[1], 2)

        buff = [b for b in target.buffs if b.__class__.__name__ == "StateBuff"][0]
        buff.when_end_turn()
        self.assertEqual(target.state[0], 5)
        self.assertEqual(target.state[1], 5)

    async def test_shadow_snare_kills_small_target(self):
        card_cls = load_card_class_from_path("pycards/Instant/Shadow_Snare/model.py", "Shadow_Snare")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Small Victim", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotEqual(env.card_zone(target), "battlefield")

    async def test_shadow_snare_controller_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Shadow_Snare/model.py", "Shadow_Snare")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Victim", 4, 4, 1)
        ctrl_life = env.p1.life

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, ctrl_life)
