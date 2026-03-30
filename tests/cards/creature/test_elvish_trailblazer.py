from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestElvish_Trailblazer(CardTestCaseBase):
    async def test_elvish_trailblazer_etb_tutors_land_to_hand(self):
        card_cls = load_card_class_from_path("pycards/creature/Elvish_Trailblazer/model.py", "Elvish_Trailblazer")
        forest_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        env = self.make_env()
        card = card_cls(env.p1)

        land = forest_cls(env.p1)
        env.p1.library = [land]
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        trailblazer = env.get_battlefield_creature(env.p1, "Elvish Trailblazer")
        self.assert_state(trailblazer, {
            "zone": "battlefield",
            "state": (2, 2),
            "flags": {"reach": True},
        })
        self.assertEqual(len(env.p1.library), 0)
        self.assertTrue(any(c.name == "Forest" for c in env.p1.hand))

    async def test_elvish_trailblazer_no_land_in_library_skips_tutor(self):
        card_cls = load_card_class_from_path("pycards/creature/Elvish_Trailblazer/model.py", "Elvish_Trailblazer")
        env = self.make_env()
        card = card_cls(env.p1)
        filler = env.create_creature(env.p1, "Nonland", 1, 1)
        env.p1.library = [filler]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.library, [filler])
        env.get_battlefield_creature(env.p1, "Elvish Trailblazer")

    async def test_elvish_trailblazer_etb_can_tutor_second_basic_when_two_in_library(self):
        card_cls = load_card_class_from_path("pycards/creature/Elvish_Trailblazer/model.py", "Elvish_Trailblazer")
        forest_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        island_cls = load_card_class_from_path("pycards/land/Island/model.py", "Island")
        env = self.make_env()
        card = card_cls(env.p1)

        first = forest_cls(env.p1)
        second = island_cls(env.p1)
        env.p1.library = [first, second]
        env.script_selection(env.p1, [1])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        hand_names = [c.name for c in env.p1.hand]
        self.assertIn("Island", hand_names)
        self.assertEqual(len(env.p1.library), 1)
        self.assertEqual(env.p1.library[0].name, "Forest")
