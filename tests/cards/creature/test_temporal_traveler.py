from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestTemporal_Traveler(CardTestCaseBase):
    async def test_temporal_traveler_base_state(self):
        card_cls = load_card_class_from_path("pycards/creature/Temporal_Traveler/model.py", "Temporal_Traveler")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        traveler = env.get_battlefield_creature(env.p1, "Temporal Traveler")
        self.assert_state(traveler, {"zone": "battlefield", "state": (3, 4)})

    async def test_temporal_traveler_attack_trigger_with_empty_graveyard_is_safe(self):
        card_cls = load_card_class_from_path("pycards/creature/Temporal_Traveler/model.py", "Temporal_Traveler")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_on_battlefield(card, env.p1)
        env.p1.graveyard = []
        before = env.snapshot()

        await env.trigger(card, "when_start_attcak", env.p2, env.p1, env.p2)
        after = env.snapshot()
        self.assertEqual(before["p1"]["graveyard"], after["p1"]["graveyard"])

    async def test_temporal_traveler_attack_ignores_non_spell_graveyard_cards(self):
        card_cls = load_card_class_from_path("pycards/creature/Temporal_Traveler/model.py", "Temporal_Traveler")
        filler_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_on_battlefield(card, env.p1)
        dead = filler_cls(env.p1)
        env.p1.graveyard = [dead]
        before_gy = [c.name for c in env.p1.graveyard]

        await env.trigger(card, "when_start_attcak", env.p2, env.p1, env.p2)
        after_gy = [c.name for c in env.p1.graveyard]
        self.assertEqual(before_gy, after_gy)
