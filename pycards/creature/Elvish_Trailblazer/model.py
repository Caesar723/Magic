
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.type_cards.land import Land
from game.type_action import actions
from game.game_function_tool import select_object


class Elvish_Trailblazer(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Elvish Trailblazer"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Elf Creature"
        self.type:str="Creature"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Elf Creature"
        self.rarity:str="Uncommon"
        self.content:str="Reach. When Elvish Trailblazer enters the battlefield, you may search your library for a basic land card, reveal it, and put it into your hand. If you do, shuffle your library."
        self.image_path:str="cards/creature/Elvish Trailblazer/image.jpg"

        self.flag_dict["reach"]=True

    @select_object("",1)
    async def when_enter_battlefield(self, player: "Player" = None, opponent: "Player" = None,selected_object:tuple['Card']=()):# when creature enter battlefield
        if selected_object:
            self.player.remove_card(selected_object[0],'library')
            self.player.append_card(selected_object[0],"hand")
            player.action_store.add_action(actions.Play_Cards(selected_object[0],player))
        

    async def selection_step(self, player: 'Player' = None, opponent: 'Player' = None, selection_random: bool = False) -> list:
        lands=[card for card in player.library if isinstance(card,Land)]
        if lands:
            card=await player.send_selection_cards(lands,selection_random)
            return [card]
        else:
            return []


        