from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.creature.Night_Stalker__.model import Night_Stalker__
from pycards.land.Forest.model import Forest


class TestOvergrowth(CardTestCaseBase):
    async def test_overgrowth_fetches_land_and_untaps_one_land(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Overgrowth/model.py", "Overgrowth")
        env = self.make_env()
        card = card_cls(env.p1)

        tapped_land = env.p1.hand.pop(0)
        env.p1.land_area.append(tapped_land)
        tapped_land.flag_dict["tap"] = True
        env.p1.library = [Forest(env.p1)]
        lands_before = len(env.p1.land_area)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), lands_before + 1)
        self.assertTrue(any(not land.get_flag("tap") for land in env.p1.land_area))
        self.assertEqual(env.p2.life, 20)

    async def test_overgrowth_untaps_without_finding_land_when_library_has_none(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Overgrowth/model.py", "Overgrowth")
        env = self.make_env()
        card = card_cls(env.p1)

        tapped_land = env.p1.hand.pop(0)
        env.p1.land_area.append(tapped_land)
        tapped_land.flag_dict["tap"] = True
        env.p1.library = [Night_Stalker__(env.p1)]
        lands_before = len(env.p1.land_area)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), lands_before)
        self.assertFalse(tapped_land.get_flag("tap"))

    async def test_overgrowth_opponent_library_unchanged(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Overgrowth/model.py", "Overgrowth")
        env = self.make_env()
        card = card_cls(env.p1)
        tapped_land = env.p1.hand.pop(0)
        env.p1.land_area.append(tapped_land)
        tapped_land.flag_dict["tap"] = True
        env.p1.library = [Forest(env.p1)]
        opp_lib_before = len(env.p2.library)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.library), opp_lib_before)
