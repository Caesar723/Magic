
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.type_cards.creature import Creature
from game.buffs import KeyBuff


class Apocalypse_Riders(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"token_power":2,"token_toughness":2,"token_count":4}

        self.fixed_id:int=182

        self.name:str="Apocalypse Riders"

        self.type:str="Sorcery"

        self.mana_cost:str="5WW"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Summon {token_count_word} {token_power}/{token_toughness} Knight creature token{token_count_plural}, each with a different ability (Trample, Haste, Lifelink, Flying)."
        self.image_path:str="cards/sorcery/Apocalypse Riders/image.jpg"



    @select_object("",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ()):
        keys=("Trample","haste","lifelink","flying")
        if self.effect_params["token_count"]>len(keys):
            raise ValueError("Each Apocalypse Rider needs a different ability")
        for key in keys[:self.effect_params["token_count"]]:
            token=self.create_token(Apocalypse_Riders_Knight,player)
            
            token.flag_dict[key]=True
            token.content=key
            player.append_card(token,"battlefield")



class Apocalypse_Riders_Knight(Creature):

    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={}

        self.name:str="Apocalypse Riders Knight"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Knight Creature - Knight"
        self.type:str="Creature"

        self.mana_cost:str="W"
        self.color:str="gold"
        self.type_card:str="Knight Creature - Knight"
        self.rarity:str="Rare"
        self.content:str=""
        self.image_path:str="cards/sorcery/Apocalypse Riders/image.jpg"




