from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestNecromancer_s_Soul_Seize(CardTestCaseBase):
    async def test_necromancer_s_soul_seize_exiles_library_and_recovers_same_type(self):
        card_cls = load_card_class_from_path("pycards/Instant/Necromancer_s_Soul_Seize/model.py", "Necromancer_s_Soul_Seize")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, env.create_creature(env.p2, "Stack", 2, 2)))
        env.p1.library = [Forest(env.p1)]
        env.p1.graveyard.append(Forest(env.p1))
        hand_before = len(env.p1.hand)

        env.room.flag_dict["bullet_time"] = True
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.exile_area), 1)
        self.assertEqual(len(env.p1.hand), hand_before + 1)

    async def test_necromancer_s_soul_seize_exiles_without_graveyard_match(self):
        """Exiled library card type with no same-type card in graveyard yields no return."""
        card_cls = load_card_class_from_path("pycards/Instant/Necromancer_s_Soul_Seize/model.py", "Necromancer_s_Soul_Seize")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, creature_cls(env.p2)))
        env.p1.library = [Forest(env.p1)]
        env.p1.graveyard.append(creature_cls(env.p1))
        hand_before = len(env.p1.hand)

        env.room.flag_dict["bullet_time"] = True
        with patch("random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.exile_area), 1)
        self.assertEqual(env.p1.exile_area[0].name, "Forest")
        self.assertEqual(len(env.p1.hand), hand_before)

    async def test_necromancer_s_soul_seize_opponent_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Necromancer_s_Soul_Seize/model.py", "Necromancer_s_Soul_Seize")
        env = self.make_env()
        card = card_cls(env.p1)
        async def _noop():
            return None
        env.room.stack.append((_noop, env.create_creature(env.p2, "Stack", 2, 2)))
        env.p1.library = [Forest(env.p1)]
        env.room.flag_dict["bullet_time"] = True
        opp = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp)
