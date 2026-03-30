from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestApocalypse_Riders(CardTestCaseBase):
    async def test_apocalypse_riders_creates_four_knights_with_distinct_keywords(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Apocalypse_Riders/model.py", "Apocalypse_Riders")
        env = self.make_env()
        card = card_cls(env.p1)

        before = len(env.p1.battlefield)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        tokens = env.p1.battlefield[before:]
        self.assertEqual(len(tokens), 4)
        contents = {t.content for t in tokens}
        self.assertEqual(contents, {"Trample", "haste", "lifelink", "flying"})
        for t in tokens:
            self.assertEqual(tuple(t.state), (2, 2))
            self.assertEqual(t.name, "Apocalypse Riders Knight")
        self.assertEqual(env.p2.life, 20)

    async def test_apocalypse_riders_only_controls_caster_battlefield(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Apocalypse_Riders/model.py", "Apocalypse_Riders")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_creatures(env.p2, "Opp Creature", 3, 3, 1)
        opp_before = len(env.p2.battlefield)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.battlefield), opp_before)

    async def test_apocalypse_riders_spell_ends_in_controller_graveyard(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Apocalypse_Riders/model.py", "Apocalypse_Riders")
        env = self.make_env()
        card = card_cls(env.p1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertTrue(any(c.name == "Apocalypse Riders" for c in env.p1.graveyard))
