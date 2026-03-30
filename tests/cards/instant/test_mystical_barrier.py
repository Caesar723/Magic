from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestMystical_Barrier(CardTestCaseBase):
    async def test_mystical_barrier_counters_and_draws(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystical_Barrier/model.py", "Mystical_Barrier")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True
        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)

    async def test_mystical_barrier_empty_library_skips_draw_after_counter(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystical_Barrier/model.py", "Mystical_Barrier")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library.clear()
        env.p1.hand.clear()
        env.put_in_hand(card, env.p1)
        hand_before = len(env.p1.hand)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before - 1)
        self.assertEqual(len(env.p1.library), 0)

    async def test_mystical_barrier_opponent_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystical_Barrier/model.py", "Mystical_Barrier")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)
        opp_life = env.p2.life

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True
        env.p1.library = [Forest(env.p1)]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_life)
