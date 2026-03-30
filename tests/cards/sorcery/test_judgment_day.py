from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestJudgment_Day(CardTestCaseBase):
    async def test_judgment_day_wipes_and_reanimates_one_each(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Judgment_Day/model.py", "Judgment_Day")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_creatures(env.p1, "Self C", 2, 2, 1)
        env.put_creatures(env.p2, "Enemy C", 2, 2, 1)

        with patch("random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), 1)
        self.assertEqual(len(env.p2.battlefield), 1)
        self.assertEqual(env.get_battlefield_creature(env.p1, "Self C").state, (2, 2))
        self.assertEqual(env.get_battlefield_creature(env.p2, "Enemy C").state, (2, 2))
        self.assertEqual(env.card_zone(card), "graveyard")

    async def test_judgment_day_only_active_player_reanimates_when_opponent_empty(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Judgment_Day/model.py", "Judgment_Day")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_creatures(env.p1, "Only One", 2, 2, 1)

        with patch("random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), 1)
        self.assertEqual(len(env.p2.battlefield), 0)
        self.assertEqual(env.get_battlefield_creature(env.p1, "Only One").state, (2, 2))

    async def test_judgment_day_empty_battlefields_skips_reanimation(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Judgment_Day/model.py", "Judgment_Day")
        env = self.make_env()
        card = card_cls(env.p1)
        self.assertEqual(len(env.p1.battlefield), 0)
        self.assertEqual(len(env.p2.battlefield), 0)

        with patch("random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), 0)
        self.assertEqual(len(env.p2.battlefield), 0)
        self.assertEqual(env.card_zone(card), "graveyard")
