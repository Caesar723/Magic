from unittest.mock import AsyncMock

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestEphemeral_Response(CardTestCaseBase):
    async def test_ephemeral_response_counters_unpaid_spell(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ephemeral_Response/model.py", "Ephemeral_Response")
        spell_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        stack_creature = spell_cls(env.p2)
        env.p2.battlefield.append(stack_creature)

        async def _noop():
            return None

        env.room.stack.append((_noop, stack_creature))
        env.room.flag_dict["bullet_time"] = True
        env.p2.mana = {"colorless": 0, "U": 0, "W": 0, "B": 0, "R": 0, "G": 0}

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(stack_creature), "graveyard")

    async def test_ephemeral_response_no_counter_when_opponent_can_pay(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ephemeral_Response/model.py", "Ephemeral_Response")
        spell_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        stack_creature = spell_cls(env.p2)
        env.p2.battlefield.append(stack_creature)

        async def _noop():
            return None

        env.room.stack.append((_noop, stack_creature))
        env.room.flag_dict["bullet_time"] = True
        env.p2.mana = {"colorless": 2, "U": 0, "W": 0, "B": 0, "R": 0, "G": 0}

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotEqual(env.card_zone(stack_creature), "graveyard")

    async def test_ephemeral_response_scry_when_countered(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ephemeral_Response/model.py", "Ephemeral_Response")
        spell_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)
        card.Scry = AsyncMock(return_value=None)

        stack_creature = spell_cls(env.p2)
        env.p2.battlefield.append(stack_creature)

        async def _noop():
            return None

        env.room.stack.append((_noop, stack_creature))
        env.room.flag_dict["bullet_time"] = True
        env.p2.mana = {"colorless": 0, "U": 0, "W": 0, "B": 0, "R": 0, "G": 0}

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        card.Scry.assert_awaited_once_with(env.p1, env.p2, 1)
