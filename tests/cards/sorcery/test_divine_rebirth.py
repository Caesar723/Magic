from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestDivine_Rebirth(CardTestCaseBase):
    async def test_divine_rebirth_returns_one_creature_from_graveyard(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Divine_Rebirth/model.py", "Divine_Rebirth")
        env = self.make_env()
        card = card_cls(env.p1)

        dead = env.create_creature(env.p1, "Dead Creature", 3, 3)
        env.p1.graveyard.append(dead)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertIn(dead, env.p1.battlefield)

    async def test_divine_rebirth_without_grave_creature_does_nothing(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Divine_Rebirth/model.py", "Divine_Rebirth")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.graveyard = []
        before = len(env.p1.battlefield)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), before)

    async def test_divine_rebirth_ignores_opponent_graveyard(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Divine_Rebirth/model.py", "Divine_Rebirth")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)
        mine = env.create_creature(env.p1, "Mine", 2, 2)
        env.p1.graveyard.append(mine)
        theirs = creature_cls(env.p2)
        env.p2.graveyard.append(theirs)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertIn(theirs, env.p2.graveyard)
        self.assertIn(mine, env.p1.battlefield)
