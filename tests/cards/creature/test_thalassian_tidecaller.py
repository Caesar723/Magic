from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestThalassian_Tidecaller(CardTestCaseBase):
    async def test_thalassian_tidecaller_draws_when_blue_spell_is_cast(self):
        card_cls = load_card_class_from_path("pycards/creature/Thalassian_Tidecaller/model.py", "Thalassian_Tidecaller")
        blue_cls = load_card_class_from_path("pycards/creature/Mistweaver_Drake/model.py", "Mistweaver_Drake")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_on_battlefield(card, env.p1)
        env.p1.library = [blue_cls(env.p1)]
        hand_before = len(env.p1.hand)

        await env.trigger(card, "when_play_a_card", blue_cls(env.p1), env.p1, env.p2)
        self.assertEqual(len(env.p1.hand), hand_before + 1)

    async def test_thalassian_tidecaller_non_blue_spell_does_not_draw(self):
        card_cls = load_card_class_from_path("pycards/creature/Thalassian_Tidecaller/model.py", "Thalassian_Tidecaller")
        red_cls = load_card_class_from_path("pycards/creature/Flame_Tinkerer/model.py", "Flame_Tinkerer")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_on_battlefield(card, env.p1)
        hand_before = len(env.p1.hand)
        await env.trigger(card, "when_play_a_card", red_cls(env.p1), env.p1, env.p2)
        self.assertEqual(len(env.p1.hand), hand_before)

    async def test_thalassian_tidecaller_does_not_fill_opponent_hand(self):
        card_cls = load_card_class_from_path("pycards/creature/Thalassian_Tidecaller/model.py", "Thalassian_Tidecaller")
        blue_cls = load_card_class_from_path("pycards/creature/Mistweaver_Drake/model.py", "Mistweaver_Drake")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_on_battlefield(card, env.p1)
        env.p1.library = [blue_cls(env.p1)]
        opp_hand_before = len(env.p2.hand)
        await env.trigger(card, "when_play_a_card", blue_cls(env.p1), env.p1, env.p2)
        self.assertEqual(len(env.p2.hand), opp_hand_before)
