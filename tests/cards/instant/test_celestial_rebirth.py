from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestCelestial_Rebirth(CardTestCaseBase):
    async def test_celestial_rebirth_returns_creature_and_grants_indestructible(self):
        card_cls = load_card_class_from_path("pycards/Instant/Celestial_Rebirth/model.py", "Celestial_Rebirth")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        dead = creature_cls(env.p1)
        env.p1.graveyard.append(dead)
        with patch("random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        revived = env.find_card_by_name(env.p1, "Night Stalker", zones=("battlefield",))
        self.assertIsNotNone(revived)
        self.assert_state(revived, {"buffs_contains": ["Indestructible"]})
        self.assertIsNotNone(env.find_card_by_name(env.p1, "Celestial Rebirth", zones=("graveyard",)))

    async def test_celestial_rebirth_empty_graveyard_resolves_without_creature(self):
        card_cls = load_card_class_from_path("pycards/Instant/Celestial_Rebirth/model.py", "Celestial_Rebirth")
        env = self.make_env()
        card = card_cls(env.p1)

        self.assertEqual(len(env.p1.graveyard), 0)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertIsNone(env.find_card_by_name(env.p1, "Night Stalker", zones=("battlefield",)))
        self.assertIsNotNone(env.find_card_by_name(env.p1, "Celestial Rebirth", zones=("graveyard",)))

    async def test_celestial_rebirth_leaves_opponent_graveyard_intact(self):
        card_cls = load_card_class_from_path("pycards/Instant/Celestial_Rebirth/model.py", "Celestial_Rebirth")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)
        mine = creature_cls(env.p1)
        env.p1.graveyard.append(mine)
        theirs = creature_cls(env.p2)
        env.p2.graveyard.append(theirs)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertIn(theirs, env.p2.graveyard)
