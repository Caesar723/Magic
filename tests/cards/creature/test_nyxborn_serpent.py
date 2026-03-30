from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestNyxborn_Serpent(CardTestCaseBase):
    async def test_nyxborn_serpent_taps_opponent_creature_on_etb(self):
        card_cls = load_card_class_from_path("pycards/creature/Nyxborn_Serpent/model.py", "Nyxborn_Serpent")
        env = self.make_env()
        card = card_cls(env.p1)
        target = env.put_creatures(env.p2, "Tap Target", 2, 2, 1)[0]

        # opponent_creatures has exactly one choice -> select index 0
        env.script_selection(env.p1, [0])
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        serpent = env.get_battlefield_creature(env.p1, "Nyxborn Serpent")
        self.assert_state(serpent, {"zone": "battlefield", "state": (3, 4)})
        self.assertTrue(target.get_flag("tap"))

    async def test_nyxborn_serpent_taps_second_creature_when_two_opponents(self):
        card_cls = load_card_class_from_path("pycards/creature/Nyxborn_Serpent/model.py", "Nyxborn_Serpent")
        env = self.make_env()
        card = card_cls(env.p1)
        first = env.put_creatures(env.p2, "First", 1, 1, 1)[0]
        second = env.put_creatures(env.p2, "Second", 2, 2, 1)[0]

        with patch(
            "game.game_function_tool.random.choice",
            side_effect=lambda seq: second if second in seq else seq[0],
        ):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertFalse(first.get_flag("tap"))
        self.assertTrue(second.get_flag("tap"))

    async def test_nyxborn_serpent_controller_life_unchanged_on_etb(self):
        card_cls = load_card_class_from_path("pycards/creature/Nyxborn_Serpent/model.py", "Nyxborn_Serpent")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Tap Target", 2, 2, 1)
        env.script_selection(env.p1, [0])
        life = env.p1.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life)
