from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest
from pycards.land.Plains.model import Plains


class TestVerdant_Genesis(CardTestCaseBase):
    async def test_verdant_genesis_puts_two_lands_and_buffs_team(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Verdant_Genesis/model.py", "Verdant_Genesis")
        env = self.make_env()
        card = card_cls(env.p1)

        c1 = env.put_creatures(env.p1, "Ally One", 2, 2, 1)[0]
        c2 = env.put_creatures(env.p1, "Ally Two", 3, 3, 1)[0]
        b1, b2 = c1.state, c2.state
        env.p1.library = [Forest(env.p1), Plains(env.p1)]
        lands_before = len(env.p1.land_area)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), lands_before + 2)
        self.assertTrue(all(l.get_flag("tap") for l in env.p1.land_area[-2:]))
        self.assertEqual(c1.state, (b1[0] + 1, b1[1] + 1))
        self.assertEqual(c2.state, (b2[0] + 1, b2[1] + 1))

    async def test_verdant_genesis_no_lands_in_library_still_buffs_creatures(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Verdant_Genesis/model.py", "Verdant_Genesis")
        env = self.make_env()
        card = card_cls(env.p1)
        c1 = env.put_creatures(env.p1, "Ally One", 2, 2, 1)[0]
        b1 = c1.state
        env.p1.library.clear()
        lands_before = len(env.p1.land_area)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), lands_before)
        self.assertEqual(c1.state, (b1[0] + 1, b1[1] + 1))

    async def test_verdant_genesis_does_not_buff_opponent_creatures(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Verdant_Genesis/model.py", "Verdant_Genesis")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "Ally", 2, 2, 1)
        foe = env.put_creatures(env.p2, "Foe", 3, 3, 1)[0]
        before = foe.state
        env.p1.library = [Forest(env.p1)]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(foe.state, before)
