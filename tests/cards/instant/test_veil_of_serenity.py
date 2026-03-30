from unittest.mock import patch
from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestVeil_of_Serenity(CardTestCaseBase):
    async def test_veil_of_serenity_exiles_target_creature(self):
        card_cls = load_card_class_from_path("pycards/Instant/Veil_of_Serenity/model.py", "Veil_of_Serenity")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Exile Me", 2, 2, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "exile_area")

    async def test_veil_of_serenity_controller_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Veil_of_Serenity/model.py", "Veil_of_Serenity")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Exile Me", 2, 2, 1)
        ctrl_life = env.p1.life

        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, ctrl_life)

    async def test_veil_of_serenity_exiles_friendly_creature_when_selected(self):
        card_cls = load_card_class_from_path("pycards/Instant/Veil_of_Serenity/model.py", "Veil_of_Serenity")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p1, "Friendly Exile", 2, 2, 1)[0]
        with patch(
            "game.game_function_tool.random.choice",
            side_effect=lambda seq: target if target in seq else seq[0],
        ):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "exile_area")
