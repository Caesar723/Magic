
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
import random
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.buffs import Tap
from game.type_cards.instant import Instant
from game.type_cards.sorcery import Sorcery

class Celestial_Skyweaver(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Celestial Skyweaver"
        self.live:int=5
        self.power:int=2
        self.actual_live:int=5
        self.actual_power:int=2

        self.type_creature:str="Spirit Creature - Spirit"
        self.type:str="Creature"

        self.mana_cost:str="2WW"
        self.color:str="gold"
        self.type_card:str="Spirit Creature - Spirit"
        self.rarity:str="Rare"
        self.content:str="Flying, Whenever you cast an instant or sorcery spell, you may tap target creature an opponent controls."
        self.image_path:str="cards/creature/Celestial Skyweaver/image.jpg"

        self.flag_dict["flying"]=True

    async def when_play_a_card(self,card:'Card',player:'Player'=None,opponent:'Player'=None):
        
        if isinstance(card,Instant) or isinstance(card,Sorcery):
            
            random_cards=[]
            for creature in opponent.battlefield:
                if creature.get_flag("tap")==False:
                    random_cards.append(creature)
            
            if random_cards:
                random_card:"Creature"=random.choice(random_cards)
                buff=Tap(self,random_card)
                random_card.gain_buff(buff,self)
                