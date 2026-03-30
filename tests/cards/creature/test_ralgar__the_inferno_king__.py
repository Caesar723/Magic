from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestRalgar__the_Inferno_King__(CardTestCaseBase):
    async def test_ralgar_etb_resolves_with_scripted_target(self):
        card_cls = load_card_class_from_path("pycards/creature/Ralgar__the_Inferno_King__/model.py", "Ralgar__the_Inferno_King__")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_creatures(env.p2, "Enemy Target", 2, 2, 1)
        env.script_selection(env.p1, [0])
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        ralgar = env.get_battlefield_creature(env.p1, "Ralgar, the Inferno King")
        self.assert_state(ralgar, {"zone": "battlefield", "state": (5, 4)})

    async def test_ralgar_gets_plus_one_power_when_casting_instant_or_sorcery(self):
        card_cls = load_card_class_from_path("pycards/creature/Ralgar__the_Inferno_King__/model.py", "Ralgar__the_Inferno_King__")
        instant_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_on_battlefield(card, env.p1)
        before = card.state
        await env.trigger(card, "when_play_a_card", instant_cls(env.p1), env.p1, env.p2)

        self.assertEqual(card.state[0], before[0] + 1)
        self.assertEqual(card.state[1], before[1])

    async def test_ralgar_creature_cast_does_not_buff_power(self):
        """Trigger is limited to instant/sorcery; a creature `card` argument does nothing."""
        card_cls = load_card_class_from_path("pycards/creature/Ralgar__the_Inferno_King__/model.py", "Ralgar__the_Inferno_King__")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_on_battlefield(card, env.p1)
        dummy_creature = env.create_creature(env.p1, "Dummy", 2, 2)
        before = card.state
        await env.trigger(card, "when_play_a_card", dummy_creature, env.p1, env.p2)
        self.assertEqual(card.state, before)
