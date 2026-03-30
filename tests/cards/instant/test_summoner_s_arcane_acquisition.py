from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestSummoner_s_Arcane_Acquisition(CardTestCaseBase):
    async def test_summoner_s_arcane_acquisition_creates_elemental_token(self):
        card_cls = load_card_class_from_path("pycards/Instant/Summoner_s_Arcane_Acquisition/model.py", "Summoner_s_Arcane_Acquisition")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertTrue(any(c.name == "Elemental Token" for c in env.p1.battlefield))

    async def test_summoner_s_arcane_acquisition_token_power_matches_spell_cost(self):
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        card_cls = load_card_class_from_path("pycards/Instant/Summoner_s_Arcane_Acquisition/model.py", "Summoner_s_Arcane_Acquisition")
        env = self.make_env()
        card = card_cls(env.p1)
        stacked = spell_cls(env.p2)
        expected = sum(stacked.cost.values())

        async def _noop():
            return None

        env.room.stack.append((_noop, stacked))
        env.room.flag_dict["bullet_time"] = True

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        token = next(c for c in env.p1.battlefield if c.name == "Elemental Token")
        self.assertEqual(token.state, (expected, expected))

    async def test_summoner_s_arcane_acquisition_controller_life_unchanged(self):
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        card_cls = load_card_class_from_path("pycards/Instant/Summoner_s_Arcane_Acquisition/model.py", "Summoner_s_Arcane_Acquisition")
        env = self.make_env()
        card = card_cls(env.p1)
        async def _noop():
            return None
        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True
        life = env.p1.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life)
