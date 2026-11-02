from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Lord_of_the_Second_Grave(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"mana_threshold":3}

        self.fixed_id:int=271

        self.name:str="Lord of the Second Grave"
        self.live:int=7
        self.power:int=7
        self.actual_live:int=7
        self.actual_power:int=7
        self.type_creature:str="Creature - Vampire Noble"
        self.type:str="Creature"
        self.mana_cost:str="6BBBB"
        self.color:str="black"
        self.type_card:str="Creature - Vampire Noble"
        self.rarity:str="Mythic Rare"
        self.content:str="Lifelink. When Lord of the Second Grave enters the battlefield, return all creature cards with mana value {mana_threshold} or less from your graveyard to the battlefield."
        self.image_path:str="cards/creature/Lord of the Second Grave/image.jpg"
        self.flag_dict["lifelink"]=True

    @select_object("",1)
    async def when_enter_battlefield(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"]=()):
        player.action_store.start_record()
        try:
            creatures=[creature for creature in player.graveyard if isinstance(creature,Creature) and sum(creature.calculate_cost().values())<=self.effect_params["mana_threshold"]]
            for creature in creatures:
                player.remove_card(creature,"graveyard")
                player.append_card(creature.copy_for_player(player),"battlefield")
        finally:
            player.action_store.end_record()
