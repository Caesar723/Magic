from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestAngelic_Protector(CardTestCaseBase):
    async def test_angelic_protector_taps_target_on_etb(self):
        protector_cls = load_card_class_from_path("pycards/creature/Angelic_Protector/model.py", "Angelic_Protector")
        env = self.make_env()
        card = protector_cls(env.p1)
        target = env.put_creatures(env.p2, "Enemy Target", 2, 2, 1)[0]

        # select the only creature target from all_creatures selection
        env.script_selection(env.p1, [0])
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        protector = env.get_battlefield_creature(env.p1, "Angelic Protector")
        self.assert_state(protector, {"zone": "battlefield", "state": (2, 2)})
        self.assertTrue(target.get_flag("tap"))

    async def test_angelic_protector_auto_select_taps_second_creature_when_patched(self):
        protector_cls = load_card_class_from_path("pycards/creature/Angelic_Protector/model.py", "Angelic_Protector")
        env = self.make_env()
        card = protector_cls(env.p1)
        first = env.put_creatures(env.p2, "Enemy A", 1, 1, 1)[0]
        second = env.put_creatures(env.p2, "Enemy B", 1, 1, 1)[0]

        def _pick_second(seq):
            self.assertGreaterEqual(len(seq), 2)
            return seq[1]

        with patch("game.game_function_tool.random.choice", side_effect=_pick_second):
            result = await env.play_card(card, env.p1)
            await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertFalse(first.get_flag("tap"))
        self.assertTrue(second.get_flag("tap"))

    async def test_angelic_protector_can_tap_friendly_creature_when_scripted(self):
        protector_cls = load_card_class_from_path("pycards/creature/Angelic_Protector/model.py", "Angelic_Protector")
        env = self.make_env()
        friend = env.put_creatures(env.p1, "Friend", 1, 1, 1)[0]
        card = protector_cls(env.p1)
        env.script_selection(env.p1, [0])
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertTrue(friend.get_flag("tap"))
        protector = env.get_battlefield_creature(env.p1, "Angelic Protector")
        self.assertFalse(protector.get_flag("tap"))
