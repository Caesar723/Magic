import types

from pycards.land.Forest.model import Forest

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestFlameblade_Pyromancer(CardTestCaseBase):
    async def test_flameblade_pyromancer_etb_can_choose_do_nothing(self):
        card_cls = load_card_class_from_path("pycards/creature/Flameblade_Pyromancer/model.py", "Flameblade_Pyromancer")
        env = self.make_env()
        card = card_cls(env.p1)

        life_before = env.p2.life
        env.script_selection(env.p1, [1])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        pyro = env.get_battlefield_creature(env.p1, "Flameblade Pyromancer")
        self.assert_state(pyro, {"zone": "battlefield", "state": (2, 2)})
        self.assertEqual(env.p2.life, life_before)

    async def test_flameblade_pyromancer_discard_deals_two_to_creature(self):
        card_cls = load_card_class_from_path("pycards/creature/Flameblade_Pyromancer/model.py", "Flameblade_Pyromancer")
        env = self.make_env()
        card = card_cls(env.p1)

        to_discard = Forest(env.p1)
        env.p1.hand.append(to_discard)
        target = env.put_creatures(env.p2, "Burn Me", 2, 2, 1)[0]

        async def _discard_then_pick_target(self, player=None, opponent=None, selection_random=False):
            player.discard(to_discard)
            return [target]

        card.selection_step = types.MethodType(_discard_then_pick_target, card)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotIn(to_discard, env.p1.hand)
        self.assertEqual(env.card_zone(target), "graveyard")

    async def test_flameblade_pyromancer_discard_can_burn_opponent(self):
        card_cls = load_card_class_from_path("pycards/creature/Flameblade_Pyromancer/model.py", "Flameblade_Pyromancer")
        env = self.make_env()
        card = card_cls(env.p1)
        to_discard = Forest(env.p1)
        env.p1.hand.append(to_discard)
        life_before = env.p2.life

        async def _discard_then_player(self, player=None, opponent=None, selection_random=False):
            player.discard(to_discard)
            return [opponent]

        card.selection_step = types.MethodType(_discard_then_player, card)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, life_before - 2)
        self.assertEqual(env.p1.life, 20)
