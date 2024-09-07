
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Nighthaunt_Assassin(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Nighthaunt Assassin"
        self.live:int=1
        self.power:int=2
        self.actual_live:int=1
        self.actual_power:int=2

        self.type_creature:str="Human Rogue"
        self.type:str="Creature"

        self.mana_cost:str="2B"
        self.color:str="black"
        self.type_card:str="Human Rogue"
        self.rarity:str="Rare"
        self.content:str="When Nighthaunt Assassin enters the battlefield, you may destroy random opponent's creature with converted mana cost 2 or less."
        self.image_path:str="cards/creature/Nighthaunt Assassin/image.jpg"



    @select_object("",1)
    async def when_enter_battlefield(self,player:'Player',opponent:'Player',selected_object:tuple['Card']=()):
        random_creatures=[]
        for creature in opponent.battlefield:
            if sum(creature.cost.values())<=2:
                random_creatures.append(creature)
        
        if random_creatures:
            random_creature:"Creature"=random.choice(random_creatures)
            await self.destroy_object(random_creature,"rgba(255,0,0,0.5)","Missile_Hit")
                