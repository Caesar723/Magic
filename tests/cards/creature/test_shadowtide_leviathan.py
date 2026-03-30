from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestShadowtide_Leviathan(CardTestCaseBase):
    async def test_shadowtide_leviathan_etb_bounces_enemy_as_new_instance(self):
        card_cls = load_card_class_from_path("pycards/creature/Shadowtide_Leviathan/model.py", "Shadowtide_Leviathan")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Enemy Target", 2, 2, 1)[0]
        hand_before = len(env.p2.hand)
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        leviathan = env.get_battlefield_creature(env.p1, "Shadowtide Leviathan")
        self.assert_state(leviathan, {"flags": {"Islandwalk": True}, "state": (8, 8)})
        self.assertEqual(len(env.p2.battlefield), 0)
        self.assertEqual(len(env.p2.hand), hand_before + 1)
        self.assertIsNot(env.p2.hand[-1], target)

    async def test_shadowtide_leviathan_empty_opponent_board_cannot_etb(self):
        """`opponent_creatures` selection yields cancel when there is no legal target."""
        card_cls = load_card_class_from_path("pycards/creature/Shadowtide_Leviathan/model.py", "Shadowtide_Leviathan")
        env = self.make_env()
        card = card_cls(env.p1)
        self.assertFalse(env.p2.battlefield)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertFalse(result[0])
        self.assertIn(card, env.p1.hand)
        self.assertIsNone(env.find_card_by_name(env.p1, "Shadowtide Leviathan", ("battlefield",)))

    async def test_shadowtide_leviathan_controller_life_unchanged_on_etb_bounce(self):
        card_cls = load_card_class_from_path("pycards/creature/Shadowtide_Leviathan/model.py", "Shadowtide_Leviathan")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Enemy Target", 2, 2, 1)
        p1_life = env.p1.life
        env.script_selection(env.p1, [0])
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, p1_life)
