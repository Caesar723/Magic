from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestMystic_Tidecaller(CardTestCaseBase):
    async def test_mystic_tidecaller_etb_bounces_creature_as_new_card(self):
        card_cls = load_card_class_from_path("pycards/creature/Mystic_Tidecaller/model.py", "Mystic_Tidecaller")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Enemy Target", 2, 2, 1)[0]
        hand_before = len(env.p2.hand)
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        tidecaller = env.get_battlefield_creature(env.p1, "Mystic Tidecaller")
        self.assert_state(tidecaller, {"zone": "battlefield", "state": (2, 3)})
        self.assertEqual(len(env.p2.battlefield), 0)
        self.assertEqual(len(env.p2.hand), hand_before + 1)
        self.assertTrue(any(c.name == "Enemy Target" for c in env.p2.hand))
        self.assertIsNot(env.p2.hand[-1], target)

    async def test_mystic_tidecaller_etb_bounces_friendly_creature(self):
        card_cls = load_card_class_from_path("pycards/creature/Mystic_Tidecaller/model.py", "Mystic_Tidecaller")
        env = self.make_env()
        card = card_cls(env.p1)

        ally = env.put_creatures(env.p1, "Friendly Ally", 1, 1, 1)[0]
        hand_before = len(env.p1.hand)
        env.script_selection(env.p1, [ally])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        tidecaller = env.get_battlefield_creature(env.p1, "Mystic Tidecaller")
        self.assert_state(tidecaller, {"zone": "battlefield", "state": (2, 3)})
        self.assertIsNotNone(env.find_card_by_name(env.p1, "Friendly Ally", zones=("hand",)))
        self.assertGreaterEqual(len(env.p1.hand), hand_before)
        bounced = env.find_card_by_name(env.p1, "Friendly Ally", zones=("hand",))
        self.assertIsNot(bounced, ally)

    async def test_mystic_tidecaller_cannot_cast_with_no_creatures_on_board(self):
        card_cls = load_card_class_from_path("pycards/creature/Mystic_Tidecaller/model.py", "Mystic_Tidecaller")
        env = self.make_env()
        card = card_cls(env.p1)
        self.assertFalse(env.p1.battlefield)
        self.assertFalse(env.p2.battlefield)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertFalse(result[0])
        self.assertIn(card, env.p1.hand)
