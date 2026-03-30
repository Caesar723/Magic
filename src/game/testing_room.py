from typing import ClassVar

from initinal_file import CARD_DICTION
from game.studio_room import Studio_Room
from game.type_cards.creature import Creature
from game.type_action import actions

# UI / message keyword (lowercase) -> engine flag_dict key
_KEYWORD_ALIASES: dict[str, str] = {
    "flying": "flying",
    "reach": "reach",
    "trample": "Trample",
    "haste": "haste",
    "lifelink": "lifelink",
    "vigilance": "Vigilance",
    "flash": "Flash",
}


class Testing_Spawn_Creature(Creature):
    """Featureless creature token for the testing lab (stats + keywords only)."""

    _seq: ClassVar[int] = 0

    def __init__(
        self,
        player,
        power: int=1,
        toughness: int=1,
        flag_keywords: dict[str, bool]={},
    ) -> None:
        super().__init__(player)
        Testing_Spawn_Creature._seq += 1
        n = Testing_Spawn_Creature._seq

        self.fixed_id = 900_000 + (n % 99_000)
        self.name = f"Test Token #{n}"
        self.live = toughness
        self.power = power
        self.actual_live = toughness
        self.actual_power = power

        self.type_creature = "Merfolk Creature"
        self.type = "Creature"
        self.mana_cost = "1"
        self.color = "blue"
        self.type_card = "Creature — Test"
        self.rarity = "Rare"
        feature_str=",".join([f"{key}" for key, val in flag_keywords.items() if val])
        self.content = f"Spawned in Testing Lab, {feature_str}"
        self.image_path = "cards/creature/Merfolk Wayfinder/image.jpg"

        for key, val in flag_keywords.items():
            if val:
                self.flag_dict[key] = True


class Testing_Room(Studio_Room):
    """
    Studio-style PVE room with extra websocket actions for manual scenario setup.
    Messages: username|test_spawn|side;power;toughness;k1,k2,...
    side is self or oppo; keywords are optional, comma-separated (see _KEYWORD_ALIASES).
    add_card: name+type+number or name+type+number+zone (zone: hand|library|graveyard).
    """

    def __init__(self, players: list[tuple], room_server) -> None:
        super().__init__(players, room_server)
        self.message_process_dict["test_spawn"] = self.test_spawn_creature
        self.message_process_dict["test_board_wipe"] = self.test_board_wipe
        self.message_process_dict["test_restore_mana"] = self.test_restore_mana
        self.message_process_dict["test_clear_hand"] = self.test_clear_hand
        self.message_process_dict["test_reset_land_cap"] = self.test_reset_land_cap
        self.message_process_dict["test_untap_all"] = self.test_untap_all

    async def add_card(self, username: str, content: str) -> None:
        """name+type+number or name+type+number+zone (hand|library|graveyard)."""
        parts = content.split("+")
        if len(parts) >= 4 and parts[-1] in ("hand", "library", "graveyard"):
            zone = parts[-1]
            try:
                number = int(parts[-2])
            except ValueError:
                return
            ctype = parts[-3]
            name = "+".join(parts[:-3])
        elif len(parts) == 3:
            name, ctype, number_s = parts
            try:
                number = int(number_s)
            except ValueError:
                return
            zone = "hand"
        else:
            return

        self.action_processor.start_record()
        for _ in range(number):
            key = f"{name}_{ctype}"
            if key in CARD_DICTION:
                card = CARD_DICTION[key](self.players[username])
                self.players[username].append_card(card, zone)
            else:
                print(f"{key} not found")
        self.action_processor.end_record()

    async def test_clear_hand(self, username: str, content: str) -> None:
        pl = self.players[username]
        self.action_processor.start_record()
        for card in list(pl.hand):
            pl.remove_card(card, "hand")
            pl.append_card(card, "graveyard")
        self.action_processor.end_record()

    async def test_reset_land_cap(self, username: str, content: str) -> None:
        self.action_processor.start_record()
        for p in (self.player_1, self.player_2):
            p.return_to_org_max_land()
        self.action_processor.end_record()

    async def test_untap_all(self, username: str, content: str) -> None:
        self.action_processor.start_record()
        for p in (self.player_1, self.player_2):
            for land in list(p.land_area):
                land.untap()
            for creature in list(p.battlefield):
                creature.untap()
        self.action_processor.end_record()

    def _parse_keywords(self, raw: str) -> dict[str, bool]:
        flags: dict[str, bool] = {}
        if not raw or not raw.strip():
            return flags
        for part in raw.split(","):
            key = part.strip().lower()
            if key in _KEYWORD_ALIASES:
                flags[_KEYWORD_ALIASES[key]] = True
        return flags

    async def test_spawn_creature(self, username: str, content: str) -> None:
        # self;power;toughness;flying,haste
        parts = content.split(";")
        if len(parts) < 3:
            return
        side = parts[0].strip().lower()
        try:
            pwr, tgh = int(parts[1]), int(parts[2])
        except ValueError:
            return
        kw_raw = parts[3] if len(parts) > 3 else ""
        flags = self._parse_keywords(kw_raw)

        human = self.players[username]
        target = human if side == "self" else human.opponent

        pwr = max(0, pwr)
        tgh = max(1, tgh)

        self.action_processor.start_record()
        creature = Testing_Spawn_Creature(target, pwr, tgh, flags)
        target.append_card(creature, "battlefield")
        self.action_processor.end_record()

    async def test_board_wipe(self, username: str, content: str) -> None:
        self.action_processor.start_record()
        for player in (self.player_1, self.player_2):
            for card in list(player.battlefield):
                card.die()
                await player.check_creature_die(card)
        self.action_processor.end_record()

    async def test_restore_mana(self, username: str, content: str) -> None:
        full = {"colorless": 0, "U": 9, "W": 9, "B": 9, "R": 9, "G": 9}
        scope = content.strip().lower() if content else "self"
        self.action_processor.start_record()
        human = self.players[username]
        targets = [human, human.opponent] if scope == "all" else [human]
        for pl in targets:
            pl.mana = dict(full)
            pl.action_store.add_action(actions.Change_Mana(pl, pl, pl.get_manas()))
        self.action_processor.end_record()
