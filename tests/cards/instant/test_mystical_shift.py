from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestMystical_Shift(CardTestCaseBase):
    async def test_mystical_shift_counters_unpaid_spell_and_draws(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystical_Shift/model.py", "Mystical_Shift")
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
        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(stack_creature), "graveyard")
        self.assertEqual(len(env.p1.hand), hand_before + 1)

    async def test_mystical_shift_opponent_pays_no_counter_no_draw(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystical_Shift/model.py", "Mystical_Shift")
        spell_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)
        stack_creature = spell_cls(env.p2)
        env.p2.battlefield.append(stack_creature)
        async def _noop():
            return None
        env.room.stack.append((_noop, stack_creature))
        env.room.flag_dict["bullet_time"] = True
        env.p2.mana = {"colorless": 5, "U": 5, "W": 0, "B": 0, "R": 0, "G": 0}
        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before)
        self.assertEqual(env.card_zone(stack_creature), "battlefield")

    async def test_mystical_shift_opponent_life_unchanged_when_countering(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystical_Shift/model.py", "Mystical_Shift")
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
        env.p1.library = [Forest(env.p1)]
        opp = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp)
