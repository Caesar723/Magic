
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.type_cards.creature import Creature
from game.game_function_tool import select_object



class Cataclysmic_Inferno(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Cataclysmic Inferno"

        self.type:str="Sorcery"

        self.mana_cost:str="3R"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Cataclysmic Inferno deals X damage to each creature your opponents control, where X is the number of Mountains you control. Then, for each creature destroyed this way, create a 1/1 red Elemental creature token with haste."
        self.image_path:str="cards/sorcery/Cataclysmic Inferno/image.jpg"

    @select_object("",1)
    async def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):# when player use the card
        colors=("rgba(255,165,0,0.9)","rgba(165, 70, 20, 0.8)","rgba(243, 0, 0, 0.9)","rgba(230, 237, 26, 0.8)","rgba(237, 68, 26, 0.8)")
        power=sum([1 for land in player.land_area if land.name=="Mountain"])
        token_counter=0
        for card in opponent.battlefield:
            player.action_store.start_record()
            
            await self.attact_to_object(card,power,random.choice(colors),"High_Missile")
            if card.check_dead():
                token_counter+=1
        for i in range(token_counter):
            player.append_card(Elemental_Creature_Cataclysmic_Inferno(player),'battlefield')


        for card in opponent.battlefield:
            player.action_store.end_record()

class Elemental_Creature_Cataclysmic_Inferno(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Elemental Creature"
        self.live:int=1
        self.power:int=1
        self.actual_live:int=1
        self.actual_power:int=1

        self.type_creature:str="Elemental Creature"
        self.type:str="Creature"

        self.mana_cost:str="R"
        self.color:str="red"
        self.type_card:str="Elemental Creature"
        self.rarity:str="Mythic Rare"
        self.content:str="haste"
        self.image_path:str="cards/sorcery/Cataclysmic Inferno/image.jpg"

        self.flag_dict["haste"]=True
