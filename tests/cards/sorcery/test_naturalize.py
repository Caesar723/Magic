from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestNaturalize(CardTestCaseBase):
    async def test_naturalize_currently_can_destroy_creature(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Naturalize/model.py", "Naturalize")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Naturalize Target", 2, 2, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "graveyard")

    async def test_naturalize_player_target_is_no_op_and_creature_untouched(self):
        """
        `all_roles` selection never includes `land_area`, so the sorcery's land branch is not
        reachable via normal `play_card` targeting. Assert current no-op behavior when a player
        is randomly chosen instead of a creature.
        """
        card_cls = load_card_class_from_path("pycards/sorcery/Naturalize/model.py", "Naturalize")
        env = self.make_env()
        card = card_cls(env.p1)
        victim = env.put_creatures(env.p2, "Safe Creature", 3, 3, 1)[0]

        with patch(
            "game.game_function_tool.random.choice",
            side_effect=lambda seq: env.p2 if env.p2 in seq else seq[0],
        ):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(victim), "battlefield")
        self.assertEqual(victim.state, (3, 3))

    async def test_naturalize_controller_life_unchanged_when_creature_destroyed(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Naturalize/model.py", "Naturalize")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Victim", 2, 2, 1)
        life_before = env.p1.life
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life_before)
