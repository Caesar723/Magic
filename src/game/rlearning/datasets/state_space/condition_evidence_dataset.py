import numpy as np
import torch

from game.rlearning.datasets.state_space.condition_event import ConditionEventDataset
from game.rlearning.states.state_space.specific_entity import CARD_ZONE_NAMES,BOARD_ZONE_NAMES


class ConditionEvidenceDataset(ConditionEventDataset):
    zone_names=(*CARD_ZONE_NAMES,*BOARD_ZONE_NAMES,"global_state")
    entity_ranges=(
        "all_roles","opponent_roles","your_roles",
        "all_creatures","opponent_creatures","your_creatures",
        "all_lands","opponent_lands","your_lands",
    )

    def get_sample(self,data):
        zone_names=self.zone_names
        result=super().get_sample(data)
        state=result["state"]
        zones={**state["card_zones"],**state["board_zones"]}
        action=int(data["action"])

        source=(-1,-1)
        if 2<=action<=11:
            source=(zone_names.index("self_board"),action-2)
        elif 12<=action<=21:
            source=(zone_names.index("self_board"),action-12)
        elif 22<=action<=31:
            source=(zone_names.index("self_land"),action-22)
        elif 32<=action<=361:
            source=(zone_names.index("hand"),(action-32)//33)

        source_id=result["supervision"].get("source_id")
        matches_source=False
        if source_id is not None and source[0]>=0:
            zone=zones[zone_names[source[0]]]
            ids=zone["card_ids"].reshape(-1)
            matches_source=source[1]<len(ids) and int(ids[source[1]])==int(source_id)

        if source_id is not None and not matches_source:
            for zone_id,name in enumerate(zone_names[:-1]):
                zone=zones[name]
                matches=np.flatnonzero(
                    (zone["card_ids"].reshape(-1)==int(source_id))
                    & zone["card_mask"].reshape(-1).astype(bool)
                )
                if len(matches):
                    source=(zone_id,int(matches[0]))
                    break

        target=(-1,-1)
        if 2<=action<=11:
            target=(zone_names.index("global_state"),1)
        elif 12<=action<=21:
            zone=zones["oppo_board"]
            matches=np.flatnonzero(
                zone["card_is_attacker"].reshape(-1)
                * zone["card_mask"].reshape(-1)
            )
            if len(matches):
                target=(zone_names.index("oppo_board"),int(matches[0]))
        elif 32<=action<=361:
            card=result["card_used"]
            scope=card.get("select_range")

            if scope is None:
                from initinal_file import CARD_DICTION

                cls=CARD_DICTION.get(card.get("card_key"))
                ability_name={
                    1:"when_enter_battlefield",
                    2:"card_ability",
                    3:"when_enter_landarea",
                    4:"card_ability",
                }.get(int(card["card_type"]),"")
                scope=getattr(getattr(cls,ability_name,None),"select_range","")

            sub=(action-32)%33
            if 1<=sub<=20 and scope in self.entity_ranges:
                enemy=sub<=10
                land=scope in ("all_lands","opponent_lands","your_lands")
                zone=("oppo_" if enemy else "self_")+("land" if land else "board")
                target=(zone_names.index(zone),sub-1 if enemy else sub-11)
            elif sub in (21,22):
                target=(zone_names.index("global_state"),1 if sub==21 else 0)

        names=("source_zone","source_slot","target_zone","target_slot")
        for name,value in zip(names,(*source,*target)):
            result[name]=np.asarray(value,dtype=np.int64)
        return result

    def collate_fn(self,batch):
        result=super().collate_fn(batch)
        for name in ("source_zone","source_slot","target_zone","target_slot"):
            result[name]=torch.from_numpy(
                np.stack([sample[name] for sample in batch])
            )
        return result