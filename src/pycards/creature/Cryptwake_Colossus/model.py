from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.type_action import actions


class Cryptwake_Colossus(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=261

        self.name:str="Cryptwake Colossus"
        self.live:int=6
        self.power:int=6
        self.actual_live:int=6
        self.actual_power:int=6
        self.type_creature:str="Creature - Giant Construct"
        self.type:str="Creature"
        self.mana_cost:str="4BBB"
        self.color:str="black"
        self.type_card:str="Creature - Giant Construct"
        self.rarity:str="Rare"
        self.content:str="Lifelink. When Cryptwake Colossus enters the battlefield, your opponent loses 3 life and you gain 3 life."
        self.image_path:str="cards/creature/Cryptwake Colossus/image.jpg"
        self.flag_dict["lifelink"]=True

    @select_object("",1)
    async def when_enter_battlefield(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            opponent.life-=3
            player.action_store.add_action(actions.Attack_To_Object(self,player,opponent,"rgba(80, 0, 120, 0.9)","Missile_Hit",[opponent.life]))
            await opponent.check_dead()
            await self.cure_to_object(player,3,"rgba(100, 220, 140, 0.9)","Cure")
        finally:
            player.action_store.end_record()
