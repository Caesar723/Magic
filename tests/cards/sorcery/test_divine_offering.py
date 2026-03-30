from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestDivine_Offering(CardTestCaseBase):
    async def test_divine_offering_casts_successfully(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Divine_Offering/model.py", "Divine_Offering")
        env = self.make_env()
        card = card_cls(env.p1)
        target = env.put_creatures(env.p2, "Offering Target", 2, 2, 1)[0]
        env.p2.life = 11

        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "graveyard")
        self.assertTrue(any(c.name == "Divine Offering" for c in env.p1.graveyard))
        self.assertEqual(env.p2.life, 14)
        self.assertEqual(env.p1.life, 20)

    async def test_divine_offering_opponent_gains_three_even_when_target_was_only_creature(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Divine_Offering/model.py", "Divine_Offering")
        env = self.make_env()
        card = card_cls(env.p1)
        lone = env.put_creatures(env.p2, "Solo Opp", 5, 5, 1)[0]
        env.p2.life = 8
        life_before = env.p2.life

        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(lone), "graveyard")
        self.assertEqual(env.p2.life, life_before + 3)

    async def test_divine_offering_only_one_enemy_creature_destroyed_when_two_present(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Divine_Offering/model.py", "Divine_Offering")
        env = self.make_env()
        card = card_cls(env.p1)
        first = env.put_creatures(env.p2, "First", 2, 2, 1)[0]
        second = env.put_creatures(env.p2, "Second", 3, 3, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(first), "graveyard")
        self.assertEqual(env.card_zone(second), "battlefield")
        self.assertEqual(second.state, (3, 3))
