from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestRavaging_Ghoul(CardTestCaseBase):
    async def test_ravaging_ghoul_etb_deals_two_to_opponent(self):
        card_cls = load_card_class_from_path("pycards/creature/Ravaging_Ghoul/model.py", "Ravaging_Ghoul")
        env = self.make_env()
        card = card_cls(env.p1)

        before_life = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, before_life - 2)
        ghoul = env.get_battlefield_creature(env.p1, "Ravaging Ghoul")
        self.assert_state(ghoul, {"zone": "battlefield", "state": (2, 2)})

    async def test_ravaging_ghoul_does_not_hurt_owner(self):
        card_cls = load_card_class_from_path("pycards/creature/Ravaging_Ghoul/model.py", "Ravaging_Ghoul")
        env = self.make_env()
        card = card_cls(env.p1)

        owner_before = env.p1.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, owner_before)

    async def test_ravaging_ghoul_etb_does_not_damage_enemy_creatures(self):
        card_cls = load_card_class_from_path("pycards/creature/Ravaging_Ghoul/model.py", "Ravaging_Ghoul")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Standing", 3, 4, 1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        standing = env.get_battlefield_creature(env.p2, "Standing")
        self.assertEqual(standing.state, (3, 4))
