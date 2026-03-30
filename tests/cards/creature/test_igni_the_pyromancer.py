from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestIgni_the_Pyromancer(CardTestCaseBase):
    async def test_igni_base_state(self):
        card_cls = load_card_class_from_path("pycards/creature/Igni_the_Pyromancer/model.py", "Igni_the_Pyromancer")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        igni = env.get_battlefield_creature(env.p1, "Igni the Pyromancer")
        self.assert_state(igni, {"zone": "battlefield", "state": (2, 2)})

    async def test_igni_damage_trigger_with_empty_graveyard_is_safe(self):
        card_cls = load_card_class_from_path("pycards/creature/Igni_the_Pyromancer/model.py", "Igni_the_Pyromancer")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_on_battlefield(card, env.p1)
        env.p1.graveyard = []
        hand_before = len(env.p1.hand)

        await env.trigger(card, "when_harm_is_done", env.p2, 1, env.p1, env.p2)
        self.assertEqual(len(env.p1.hand), hand_before)

    async def test_igni_damage_to_creature_does_not_cast_from_graveyard(self):
        card_cls = load_card_class_from_path("pycards/creature/Igni_the_Pyromancer/model.py", "Igni_the_Pyromancer")
        env = self.make_env()
        card = card_cls(env.p1)

        foe = env.put_creatures(env.p2, "Foe", 3, 3, 1)[0]
        env.put_on_battlefield(card, env.p1)
        instant_cls = load_card_class_from_path("pycards/Instant/Aquatic_Evasion/model.py", "Aquatic_Evasion")
        env.p1.graveyard.append(instant_cls(env.p1))
        hand_before = len(env.p1.hand)

        await env.trigger(card, "when_harm_is_done", foe, 1, env.p1, env.p2)

        self.assertEqual(len(env.p1.hand), hand_before)
