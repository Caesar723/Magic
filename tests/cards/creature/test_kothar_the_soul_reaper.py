from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestKothar_the_Soul_Reaper(CardTestCaseBase):
    async def test_kothar_etb_forces_opponent_sacrifice(self):
        card_cls = load_card_class_from_path("pycards/creature/Kothar_the_Soul_Reaper/model.py", "Kothar_the_Soul_Reaper")
        env = self.make_env()
        card = card_cls(env.p1)

        enemy = env.put_creatures(env.p2, "Enemy Target", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotEqual(env.card_zone(enemy), "battlefield")

    async def test_kothar_gets_plus_one_plus_one_when_creature_dies(self):
        card_cls = load_card_class_from_path("pycards/creature/Kothar_the_Soul_Reaper/model.py", "Kothar_the_Soul_Reaper")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_on_battlefield(card, env.p1)
        before = card.state
        dead = env.create_creature(env.p2, "Dead Creature", 3, 3)
        await env.trigger(card, "when_a_creature_die", dead, env.p1, env.p2)

        self.assertEqual(card.state, (before[0] + 1, before[1] + 1))

    async def test_kothar_etb_with_empty_opponent_battlefield_safe(self):
        card_cls = load_card_class_from_path("pycards/creature/Kothar_the_Soul_Reaper/model.py", "Kothar_the_Soul_Reaper")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p2.battlefield.clear()

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        env.get_battlefield_creature(env.p1, "Kothar the Soul Reaper")

    async def test_kothar_etb_sacrifices_one_creature_when_opponent_has_two(self):
        card_cls = load_card_class_from_path("pycards/creature/Kothar_the_Soul_Reaper/model.py", "Kothar_the_Soul_Reaper")
        env = self.make_env()
        card = card_cls(env.p1)
        a = env.put_creatures(env.p2, "Sac A", 1, 1, 1)[0]
        b = env.put_creatures(env.p2, "Sac B", 2, 2, 1)[0]

        with patch("random.choice", lambda bf: a):
            result = await env.play_card(card, env.p1)
            await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(a), "graveyard")
        self.assertIn(b, env.p2.battlefield)
        self.assertEqual(len(env.p2.battlefield), 1)
