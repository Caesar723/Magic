from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Island.model import Island


class TestMystic_Tide(CardTestCaseBase):
    async def test_mystic_tide_counters_and_can_bounce_with_island(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Tide/model.py", "Mystic_Tide")
        spell_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        stack_creature = spell_cls(env.p2)
        env.p2.battlefield.append(stack_creature)
        env.p1.land_area.append(Island(env.p1))
        env.put_creatures(env.p2, "Bounce Target", 2, 2, 1)

        async def _noop():
            return None

        env.room.stack.append((_noop, stack_creature))
        env.room.flag_dict["bullet_time"] = True
        env.p2.mana = {"colorless": 0, "U": 0, "W": 0, "B": 0, "R": 0, "G": 0}
        p2_hand_before = len(env.p2.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertGreaterEqual(len(env.p2.hand), p2_hand_before + 1)
        self.assertEqual(env.p1.life, 20)
        self.assertTrue(any(getattr(l, "name", "") == "Island" for l in env.p1.land_area))

    async def test_mystic_tide_counters_without_bounce_when_no_island(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Tide/model.py", "Mystic_Tide")
        spell_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        stack_creature = spell_cls(env.p2)
        env.p2.battlefield.append(stack_creature)
        env.put_creatures(env.p2, "Bounce Target", 2, 2, 1)

        async def _noop():
            return None

        env.room.stack.append((_noop, stack_creature))
        env.room.flag_dict["bullet_time"] = True
        env.p2.mana = {"colorless": 0, "U": 0, "W": 0, "B": 0, "R": 0, "G": 0}
        p2_hand_before = len(env.p2.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(stack_creature), "graveyard")
        self.assertEqual(len(env.p2.hand), p2_hand_before)

    async def test_mystic_tide_counter_and_bounce_paths_leave_opponent_life(self):
        spell_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Tide/model.py", "Mystic_Tide")
        env = self.make_env()
        card = card_cls(env.p1)
        stack_creature = spell_cls(env.p2)
        env.p2.battlefield.append(stack_creature)
        env.p1.land_area.append(Island(env.p1))
        env.put_creatures(env.p2, "By", 1, 1, 1)
        env.p2.mana = {"colorless": 0, "U": 0, "W": 0, "B": 0, "R": 0, "G": 0}
        opp_life = env.p2.life

        async def _noop():
            return None

        env.room.stack.append((_noop, stack_creature))
        env.room.flag_dict["bullet_time"] = True
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_life)
