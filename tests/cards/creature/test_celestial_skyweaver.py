from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestCelestial_Skyweaver(CardTestCaseBase):
    async def test_celestial_skyweaver_has_flying(self):
        card_cls = load_card_class_from_path("pycards/creature/Celestial_Skyweaver/model.py", "Celestial_Skyweaver")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        skyweaver = env.get_battlefield_creature(env.p1, "Celestial Skyweaver")
        self.assert_state(skyweaver, {
            "zone": "battlefield",
            "state": (2, 5),
            "flags": {"flying": True},
        })

    async def test_celestial_skyweaver_taps_opponent_creature_on_instant_cast(self):
        creature_cls = load_card_class_from_path("pycards/creature/Celestial_Skyweaver/model.py", "Celestial_Skyweaver")
        instant_cls = load_card_class_from_path("pycards/Instant/Aquatic_Evasion/model.py", "Aquatic_Evasion")
        env = self.make_env()

        skyweaver = creature_cls(env.p1)
        victim = env.put_creatures(env.p2, "Tap Victim", 2, 2, 1)[0]

        result = await env.play_card(skyweaver, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        spell = instant_cls(env.p1)
        await env.play_card(spell, env.p1, selections=[0])
        await env.resolve_stack()

        self.assertTrue(victim.get_flag("tap"))

    async def test_celestial_skyweaver_instant_cast_no_opponent_creatures_no_error(self):
        creature_cls = load_card_class_from_path("pycards/creature/Celestial_Skyweaver/model.py", "Celestial_Skyweaver")
        instant_cls = load_card_class_from_path("pycards/Instant/Aquatic_Evasion/model.py", "Aquatic_Evasion")
        env = self.make_env()
        env.p2.battlefield.clear()

        skyweaver = creature_cls(env.p1)
        result = await env.play_card(skyweaver, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        spell = instant_cls(env.p1)
        await env.play_card(spell, env.p1, selections=[0])
        await env.resolve_stack()

        self.assertEqual(len(env.p2.battlefield), 0)

    async def test_celestial_skyweaver_creature_spell_cast_does_not_tap_opponent(self):
        creature_cls = load_card_class_from_path("pycards/creature/Celestial_Skyweaver/model.py", "Celestial_Skyweaver")
        squire_cls = load_card_class_from_path("pycards/creature/Elite_Squire/model.py", "Elite_Squire")
        env = self.make_env()

        skyweaver = creature_cls(env.p1)
        victim = env.put_creatures(env.p2, "Tap Victim", 2, 2, 1)[0]

        result = await env.play_card(skyweaver, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        extra = squire_cls(env.p1)
        env.put_in_hand(extra, env.p1)
        await env.play_card(extra, env.p1)
        await env.resolve_stack()

        self.assertFalse(victim.get_flag("tap"))
        self.assertEqual(len([c for c in env.p1.battlefield if c.name == "Elite Squire"]), 1)
