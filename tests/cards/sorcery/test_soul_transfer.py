from unittest.mock import patch

from pycards.land.Forest.model import Forest

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestSoul_Transfer(CardTestCaseBase):
    async def test_soul_transfer_grants_die_ability_buff_from_graveyard(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Soul_Transfer/model.py", "Soul_Transfer")
        phoenix_cls = load_card_class_from_path("pycards/creature/Eternal_Phoenix/model.py", "Eternal_Phoenix")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p1, "Recipient", 2, 2, 1)[0]
        env.p1.graveyard.append(phoenix_cls(env.p1))

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(target, {"buffs_contains": ["Soul_Transfer_buff"]})

    async def test_soul_transfer_with_only_noncreature_graveyard_still_buffs_target(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Soul_Transfer/model.py", "Soul_Transfer")
        env = self.make_env()
        card = card_cls(env.p1)
        target = env.put_creatures(env.p1, "Recipient", 2, 2, 1)[0]
        env.p1.graveyard.append(Forest(env.p1))

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(target, {"buffs_contains": ["Soul_Transfer_buff"]})

    async def test_soul_transfer_does_not_buff_opponent_when_targeting_friendly(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Soul_Transfer/model.py", "Soul_Transfer")
        phoenix_cls = load_card_class_from_path("pycards/creature/Eternal_Phoenix/model.py", "Eternal_Phoenix")
        env = self.make_env()
        card = card_cls(env.p1)

        recipient = env.put_creatures(env.p1, "Recipient", 2, 2, 1)[0]
        foe = env.put_creatures(env.p2, "Foe", 2, 2, 1)[0]
        env.p1.graveyard.append(phoenix_cls(env.p1))

        with patch(
            "game.game_function_tool.random.choice",
            side_effect=lambda seq: recipient if recipient in seq else seq[0],
        ):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(recipient, {"buffs_contains": ["Soul_Transfer_buff"]})
        self.assertEqual(foe.buffs, [])
