from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestMystic_Reflection(CardTestCaseBase):
    async def test_mystic_reflection_copies_named_twin_until_end_turn(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Reflection/model.py", "Mystic_Reflection")
        env = self.make_env()
        card = card_cls(env.p1)

        source = env.create_creature(env.p1, "Mirror Entity", 5, 5)
        twin = env.create_creature(env.p1, "Mirror Entity", 2, 2)
        env.put_on_battlefield(source, env.p1)
        env.put_on_battlefield(twin, env.p1)

        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: source if source in seq else seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(twin.state[0], source.state[0])
        self.assertEqual(twin.state[1], source.state[1])

        copy_buffs = [b for b in twin.buffs if b.__class__.__name__ == "Mystic_Reflection_Copy_Buff"]
        self.assertEqual(len(copy_buffs), 1)
        copy_buffs[0].when_end_turn()
        self.assertEqual(twin.state[0], 2)
        self.assertEqual(twin.state[1], 2)

    async def test_mystic_reflection_no_same_name_copy_target_skipped(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Reflection/model.py", "Mystic_Reflection")
        env = self.make_env()
        card = card_cls(env.p1)
        solo = env.create_creature(env.p1, "Unique Solo", 3, 3)
        env.put_on_battlefield(solo, env.p1)
        env.script_selection(env.p1, [0])
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(solo.state, (3, 3))
        self.assertEqual(
            [b for b in solo.buffs if b.__class__.__name__ == "Mystic_Reflection_Copy_Buff"],
            [],
        )

    async def test_mystic_reflection_can_copy_opponent_same_name_creature(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Reflection/model.py", "Mystic_Reflection")
        env = self.make_env()
        card = card_cls(env.p1)
        source = env.create_creature(env.p1, "Shared Name", 6, 6)
        twin_opp = env.create_creature(env.p2, "Shared Name", 1, 9)
        env.put_on_battlefield(source, env.p1)
        env.put_on_battlefield(twin_opp, env.p2)
        env.script_selection(env.p1, [source, twin_opp])
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(twin_opp.state[0], source.state[0])
        self.assertEqual(twin_opp.state[1], source.state[1])
        self.assertEqual(env.p1.life, 20)
