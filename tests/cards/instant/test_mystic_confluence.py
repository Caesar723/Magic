from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestMystic_Confluence(CardTestCaseBase):
    async def test_mystic_confluence_bounces_creature_and_draws(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Confluence/model.py", "Mystic_Confluence")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Bounce Me", 2, 2, 1)[0]
        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)
        opp_hand_before = len(env.p2.hand)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)
        self.assertEqual(len(env.p2.hand), opp_hand_before + 1)
        self.assertIsNot(env.p2.hand[-1], target)

    async def test_mystic_confluence_draws_when_opponent_battlefield_empty(self):
        """No creatures to bounce; counter still runs if stack has a spell; draw still happens."""
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Confluence/model.py", "Mystic_Confluence")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)
        self.assertEqual(len(env.p2.battlefield), 0)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)

    async def test_mystic_confluence_opponent_library_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Confluence/model.py", "Mystic_Confluence")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "B", 1, 1, 1)
        env.p1.library = [Forest(env.p1)]
        opp_lib_before = len(env.p2.library)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.library), opp_lib_before)
