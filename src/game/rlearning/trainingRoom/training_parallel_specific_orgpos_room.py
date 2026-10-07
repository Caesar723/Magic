from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room

class Multi_Agent_Parallel_Specific_Orgpos_Room(Multi_Agent_Parallel_Specific_Room):

    def all_play_card_messages(self, player):
        name = player.name
        messages = []
        # sub_action=0: 无目标
        messages.append(f"{name}|play_card|0")
        # sub_action 1-10: 敌方生物
        for rank in range(10):
            if rank < len(player.opponent.battlefield):
                idx = rank
                sel = f"{name}|field|opponent_battlefield|{idx}"
                messages.append(f"{name}|play_card|0||{sel}")
        # sub_action 11-20: 我方生物
        for rank in range(10):
            if rank < len(player.battlefield):
                idx = rank
                sel = f"{name}|field|self_battlefield|{idx}"
                messages.append(f"{name}|play_card|0||{sel}")
        # sub_action 21-22: 英雄
        messages.append(f"{name}|play_card|0||{name}|field|oppo|")
        messages.append(f"{name}|play_card|0||{name}|field|self|")
        # sub_action 23-32: 选手牌
        for card_idx in range(12, 22):
            sel = f"{name}|cards|{card_idx}|"
            messages.append(f"{name}|play_card|0||{sel}")
        return messages
