from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestMechanist_s_Disruption_Device(CardTestCaseBase):
    async def test_mechanist_s_disruption_device_draws_and_puts_land(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mechanist_s_Disruption_Device/model.py", "Mechanist_s_Disruption_Device")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, env.create_creature(env.p2, "Stack", 2, 2)))
        land = Forest(env.p1)
        env.p1.hand.append(land)
        env.p1.library = [Forest(env.p1)]
        lands_before = len(env.p1.land_area)
        env.room.flag_dict["bullet_time"] = True
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertGreaterEqual(len(env.p1.land_area), lands_before + 1)

    async def test_mechanist_disruption_draw_only_when_hand_has_no_land(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mechanist_s_Disruption_Device/model.py", "Mechanist_s_Disruption_Device")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.p1.hand = [c for c in env.p1.hand if getattr(c, "type", "") != "Land"]
        hand_before = len(env.p1.hand)
        env.p1.library = [spell_cls(env.p1)]
        lands_before = len(env.p1.land_area)
        env.room.flag_dict["bullet_time"] = True
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), lands_before)
        self.assertEqual(len(env.p1.hand), hand_before + 1)

    async def test_mechanist_disruption_opponent_life_and_lands_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mechanist_s_Disruption_Device/model.py", "Mechanist_s_Disruption_Device")
        env = self.make_env()
        card = card_cls(env.p1)
        opp_lands_before = len(env.p2.land_area)
        opp_life = env.p2.life

        async def _noop():
            return None

        env.room.stack.append((_noop, env.create_creature(env.p2, "Stack", 2, 2)))
        env.p1.hand = [c for c in env.p1.hand if getattr(c, "type", "") != "Land"]
        env.p1.library = [Forest(env.p1)]
        env.room.flag_dict["bullet_time"] = True
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_life)
        self.assertEqual(len(env.p2.land_area), opp_lands_before)
