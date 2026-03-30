from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestFiery_Blast(CardTestCaseBase):
    async def test_fiery_blast_deals_two_to_player(self):
        card_cls = load_card_class_from_path("pycards/Instant/Fiery_Blast/model.py", "Fiery_Blast")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.life = 10
        env.p2.life = 10
        before_p1 = env.p1.life
        before_p2 = env.p2.life
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[-1]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertIn((env.p1.life, env.p2.life), {(before_p1 - 2, before_p2), (before_p1, before_p2 - 2)})

    async def test_fiery_blast_deals_two_to_creature(self):
        card_cls = load_card_class_from_path("pycards/Instant/Fiery_Blast/model.py", "Fiery_Blast")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p1, "Burn Target", 2, 3, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(target.state[1], 1)
        self.assertEqual(env.p2.life, 20)

    async def test_fiery_blast_lethal_sends_creature_to_graveyard(self):
        card_cls = load_card_class_from_path("pycards/Instant/Fiery_Blast/model.py", "Fiery_Blast")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Fragile", 1, 2, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "graveyard")
