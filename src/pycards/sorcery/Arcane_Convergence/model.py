
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.type_action import actions

class Arcane_Convergence(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=183

        self.name:str="Arcane Convergence"

        self.type:str="Sorcery"

        self.mana_cost:str="3UU"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Arcane Convergence allows you to untap all lands you control and add X mana in any combination of colors to your mana pool, where X is the number of sorcery cards in your graveyard."
        self.image_path:str="cards/sorcery/Arcane Convergence/image.jpg"

    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        for land in player.land_area:
            if land.get_flag("tap"):
                land.untap()
        sorceries = player.get_cards_by_pos_type("graveyard",(Sorcery,))
        mana_count=len(sorceries)
        while mana_count>0:
            for key in ["U","B","R","G","W"]:
                player.mana[key]+= 1
                mana_count-=1
                if mana_count<=0:
                    break
            

        player.action_store.add_action(actions.Change_Mana(self, player, player.get_manas()))




        