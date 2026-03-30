from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestFlamespark(CardTestCaseBase):
    async def test_flamespark_deals_three_without_mountain(self):
        card_cls = load_card_class_from_path("pycards/Instant/Flamespark/model.py", "Flamespark")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Spark Target", 2, 5, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(target.state[1], 2)

    async def test_flamespark_deals_five_with_mountain(self):
        card_cls = load_card_class_from_path("pycards/Instant/Flamespark/model.py", "Flamespark")
        env = self.make_env()
        card = card_cls(env.p1)

        mountain = None
        for zone_name in ("hand", "library"):
            zone = getattr(env.p1, zone_name)
            for c in list(zone):
                if c.name == "Mountain":
                    zone.remove(c)
                    mountain = c
                    break
            if mountain:
                break
        self.assertIsNotNone(mountain)
        env.p1.land_area.append(mountain)

        target = env.put_creatures(env.p2, "Spark Target", 2, 5, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "graveyard")

    async def test_flamespark_can_target_player_for_three(self):
        card_cls = load_card_class_from_path("pycards/Instant/Flamespark/model.py", "Flamespark")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.life = 20
        env.p2.life = 20
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[-1]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertTrue(env.p1.life == 17 or env.p2.life == 17)
