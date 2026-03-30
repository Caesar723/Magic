from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.creature.Night_Stalker__.model import Night_Stalker__
from pycards.land.Forest.model import Forest
from pycards.land.Island.model import Island


class TestThornroot_Druid(CardTestCaseBase):
    async def test_thornroot_druid_etb_puts_basic_land_into_hand(self):
        card_cls = load_card_class_from_path("pycards/creature/Thornroot_Druid/model.py", "Thornroot_Druid")
        env = self.make_env()
        card = card_cls(env.p1)

        known_land = Forest(env.p1)
        env.p1.library = [known_land]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        druid = env.get_battlefield_creature(env.p1, "Thornroot Druid")
        self.assert_state(druid, {"zone": "battlefield", "state": (2, 2)})
        self.assertEqual(len(env.p1.library), 0)
        self.assertTrue(any(c.name == "Forest" for c in env.p1.hand))

    async def test_thornroot_druid_no_basic_in_library_skips_tutor(self):
        card_cls = load_card_class_from_path("pycards/creature/Thornroot_Druid/model.py", "Thornroot_Druid")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.hand.clear()
        env.p1.library = [Night_Stalker__(env.p1)]
        lib_before = len(env.p1.library)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.library), lib_before)
        self.assertFalse(any(getattr(c, "name", "") == "Forest" for c in env.p1.hand))

    async def test_thornroot_druid_etb_can_tutor_island_when_multiple_basics_in_library(self):
        card_cls = load_card_class_from_path("pycards/creature/Thornroot_Druid/model.py", "Thornroot_Druid")
        env = self.make_env()
        card = card_cls(env.p1)
        island = Island(env.p1)
        forest = Forest(env.p1)
        env.p1.library = [forest, island]

        with patch("random.choice", lambda seq: island), patch("random.shuffle", lambda _lib: None):
            result = await env.play_card(card, env.p1)
            await env.resolve_stack()

        self.assertTrue(result[0])
        hand_names = [c.name for c in env.p1.hand]
        self.assertIn("Island", hand_names)
        self.assertEqual(len(env.p1.library), 1)
