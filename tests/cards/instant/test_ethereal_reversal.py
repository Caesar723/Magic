from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestEthereal_Reversal(CardTestCaseBase):
    async def test_ethereal_reversal_bounces_and_casts_small_spell(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ethereal_Reversal/model.py", "Ethereal_Reversal")
        spell_cls = load_card_class_from_path("pycards/Instant/Mystic_Insight/model.py", "Mystic_Insight")
        ns_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        target = ns_cls(env.p2)
        env.put_on_battlefield(target, env.p2)
        spell = spell_cls(env.p1)
        env.p1.hand.append(spell)
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        bounced = env.find_card_by_name(env.p2, "Night Stalker", zones=("hand",))
        self.assertIsNotNone(bounced)
        self.assertEqual(bounced.player, env.p2)
        self.assertIsNotNone(env.find_card_by_name(env.p1, "Mystic Insight", zones=("graveyard",)))

    async def test_ethereal_reversal_zero_mv_bounce_does_not_cast_hand_spell(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ethereal_Reversal/model.py", "Ethereal_Reversal")
        spell_cls = load_card_class_from_path("pycards/Instant/Mystic_Insight/model.py", "Mystic_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Zero MV", 1, 1, 1)[0]
        self.assertEqual(sum(target.cost.values()), 0)
        spell = spell_cls(env.p1)
        env.p1.hand.append(spell)

        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        bounced = env.find_card_by_name(env.p2, "Zero MV", zones=("hand",))
        self.assertIsNotNone(bounced)
        self.assertIn(spell, env.p1.hand)
        self.assertIsNone(env.find_card_by_name(env.p1, "Mystic Insight", zones=("graveyard",)))

    async def test_ethereal_reversal_bounce_paths_leave_controller_life(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ethereal_Reversal/model.py", "Ethereal_Reversal")
        spell_cls = load_card_class_from_path("pycards/Instant/Mystic_Insight/model.py", "Mystic_Insight")
        ns_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)
        target = ns_cls(env.p2)
        env.put_on_battlefield(target, env.p2)
        env.p1.hand.append(spell_cls(env.p1))
        life_before = env.p1.life
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life_before)
