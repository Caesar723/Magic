from unittest.mock import AsyncMock

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestMistweaver_Adept(CardTestCaseBase):
    async def test_mistweaver_adept_base_stats(self):
        card_cls = load_card_class_from_path("pycards/creature/Mistweaver_Adept/model.py", "Mistweaver_Adept")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        adept = env.get_battlefield_creature(env.p1, "Mistweaver Adept")
        self.assert_state(adept, {"zone": "battlefield", "state": (2, 1)})

    async def test_mistweaver_adept_optional_trigger_can_do_nothing(self):
        card_cls = load_card_class_from_path("pycards/creature/Mistweaver_Adept/model.py", "Mistweaver_Adept")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _skip_selection(player=None, opponent=None, selection_random=False):
            return [card.create_selection("Do nothing", 2)]

        card.selection_step = _skip_selection
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.battlefield), 0)

    async def test_mistweaver_adept_etb_bounce_and_scry(self):
        card_cls = load_card_class_from_path("pycards/creature/Mistweaver_Adept/model.py", "Mistweaver_Adept")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Enemy Target", 2, 2, 1)[0]
        hand_before = len(env.p2.hand)

        async def _pick_target(player=None, opponent=None, selection_random=False):
            return [target]

        card.selection_step = _pick_target

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.battlefield), 0)
        self.assertEqual(len(env.p2.hand), hand_before + 1)
        self.assertTrue(any(c.name == "Enemy Target" for c in env.p2.hand))
        self.assertIsNot(env.p2.hand[-1], target)

    async def test_mistweaver_adept_bounce_path_calls_scry_two(self):
        card_cls = load_card_class_from_path("pycards/creature/Mistweaver_Adept/model.py", "Mistweaver_Adept")
        env = self.make_env()
        card = card_cls(env.p1)
        card.Scry = AsyncMock(return_value=None)

        target = env.put_creatures(env.p2, "Bounce Me", 1, 1, 1)[0]

        async def _pick_target(player=None, opponent=None, selection_random=False):
            return [target]

        card.selection_step = _pick_target

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        card.Scry.assert_awaited_once_with(env.p1, env.p2, 2)
