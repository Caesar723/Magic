from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestVeiled_Concealment(CardTestCaseBase):
    async def test_veiled_concealment_smoke(self):
        card_cls = load_card_class_from_path("pycards/Instant/Veiled_Concealment/model.py", "Veiled_Concealment")
        env = self.make_env()
        card = card_cls(env.p1)

        before = env.snapshot()
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        after = env.snapshot()

        # basic run assertions
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(before, dict)
        self.assertIsInstance(after, dict)

    async def test_veiled_concealment_custom_scenario_template(self):
        """Edit this test to set exact expected before/after state."""
        card_cls = load_card_class_from_path("pycards/Instant/Veiled_Concealment/model.py", "Veiled_Concealment")
        env = self.make_env()
        card = card_cls(env.p1)

        # 1) Setup custom scene before using card
        # Example:
        # env.p1.life = 10
        # env.put_in_hand(card, env.p1)
        before = env.snapshot()

        # 2) Trigger card usage / effect
        await env.play_card(card, env.p1)
        await env.resolve_stack()
        # Optional: simulate turns
        # await env.advance_turns(2)

        # 3) Assert expected state after effect
        after = env.snapshot()
        expected_after = {
            # "p1": {"life": 20},
            # "p2": {"life": 18},
        }
        self.assert_partial_state(after, expected_after)
        self.assertIsInstance(before, dict)
