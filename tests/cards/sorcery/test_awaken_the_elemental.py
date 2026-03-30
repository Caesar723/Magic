from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestAwaken_the_Elemental(CardTestCaseBase):
    async def test_awaken_the_elemental_returns_grave_creature_and_buffs(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Awaken_the_Elemental/model.py", "Awaken_the_Elemental")
        dead_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        dead = dead_cls(env.p1)
        env.p1.graveyard.append(dead)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        revived = next(c for c in env.p1.battlefield if c.name == "Night Stalker")
        self.assertGreaterEqual(revived.state[0], 6)
        self.assertGreaterEqual(revived.state[1], 6)
        self.assertIn(dead, env.p1.graveyard)
        self.assertIsNot(revived, dead)

    async def test_awaken_the_elemental_empty_graveyard_no_new_creature(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Awaken_the_Elemental/model.py", "Awaken_the_Elemental")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.graveyard.clear()
        bf_before = len(env.p1.battlefield)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), bf_before)

    async def test_awaken_the_elemental_does_not_use_opponent_graveyard(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Awaken_the_Elemental/model.py", "Awaken_the_Elemental")
        dead_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        only_opp = dead_cls(env.p2)
        env.p2.graveyard.append(only_opp)
        env.p1.graveyard.clear()
        bf_before = len(env.p1.battlefield)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), bf_before)
        self.assertIn(only_opp, env.p2.graveyard)
