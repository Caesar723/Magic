from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import AsyncMock


class TestTemporal_Flux(CardTestCaseBase):
    async def test_temporal_flux_adds_extra_turn_counter(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Temporal_Flux/model.py", "Temporal_Flux")
        env = self.make_env()
        card = card_cls(env.p1)
        card.Scry = AsyncMock(return_value=None)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(env.p1, {"counters": {"extra_turn": 1}})
        card.Scry.assert_awaited_once_with(env.p1, env.p2, 2)

    async def test_temporal_flux_stacks_extra_turn_counter(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Temporal_Flux/model.py", "Temporal_Flux")
        env = self.make_env()
        env.p1.add_counter_dict("extra_turn", 3)
        card = card_cls(env.p1)
        card.Scry = AsyncMock(return_value=None)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(env.p1, {"counters": {"extra_turn": 4}})
        card.Scry.assert_awaited_once()

    async def test_temporal_flux_does_not_increment_opponent_extra_turn(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Temporal_Flux/model.py", "Temporal_Flux")
        env = self.make_env()
        card = card_cls(env.p1)
        card.Scry = AsyncMock(return_value=None)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.counter_dict.get("extra_turn", 0), 0)
