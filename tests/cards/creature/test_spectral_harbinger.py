from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestSpectral_Harbinger(CardTestCaseBase):
    async def test_spectral_harbinger_etb_exiles_grave_creature_and_gains_life(self):
        card_cls = load_card_class_from_path("pycards/creature/Spectral_Harbinger/model.py", "Spectral_Harbinger")
        env = self.make_env()
        card = card_cls(env.p1)

        dead = env.create_creature(env.p1, "Dead Creature", 2, 2)
        env.p1.graveyard.append(dead)
        env.p1.life = 10
        life_before = env.p1.life

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        harbinger = env.get_battlefield_creature(env.p1, "Spectral Harbinger")
        self.assert_state(harbinger, {"flags": {"flying": True, "lifelink": True}, "state": (2, 3)})
        self.assertEqual(len(env.p1.graveyard), 0)
        self.assertEqual(env.p1.life, life_before + 2)
        self.assertEqual(env.p2.life, 20)

    async def test_spectral_harbinger_empty_graveyard_etb_no_life_gain(self):
        card_cls = load_card_class_from_path("pycards/creature/Spectral_Harbinger/model.py", "Spectral_Harbinger")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.life = 10
        self.assertEqual(len(env.p1.graveyard), 0)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        harbinger = env.get_battlefield_creature(env.p1, "Spectral Harbinger")
        self.assert_state(harbinger, {"zone": "battlefield", "flags": {"flying": True, "lifelink": True}})
        self.assertEqual(env.p1.life, 10)

    async def test_spectral_harbinger_does_not_exile_from_opponent_graveyard(self):
        card_cls = load_card_class_from_path("pycards/creature/Spectral_Harbinger/model.py", "Spectral_Harbinger")
        env = self.make_env()
        card = card_cls(env.p1)
        dead_opp = env.create_creature(env.p2, "Opp Dead", 2, 2)
        env.p2.graveyard.append(dead_opp)
        env.p1.life = 10
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertIn(dead_opp, env.p2.graveyard)
