
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.type_cards.land import Land
from game.game_function_tool import select_object
from game.buffs import Infect

class Vorinclex__Apex_of_Mutation(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Vorinclex, Apex of Mutation"
        self.live:int=6
        self.power:int=6
        self.actual_live:int=6
        self.actual_power:int=6

        self.type_creature:str="Legendary Creature - Phyrexian Mutant"
        self.type:str="Creature"

        self.mana_cost:str="3GG"
        self.color:str="green"
        self.type_card:str="Legendary Creature - Phyrexian Mutant"
        self.rarity:str="Mythic Rare"
        self.content:str="Trample, Infect, and whenever you cast a spell, proliferate for three random permanent. Whenever an opponent proliferates, they must pay 2 life for each permanent ."
        self.image_path:str="cards/creature/Vorinclex, Apex of Mutation/image.jpg"

        self.flag_dict['Trample']=True
        buff=Infect(self,self)
        self.gain_buff(buff,self)

    async def when_play_a_card(self,card:'Card',player:'Player'=None,opponent:'Player'=None):
        if self in player.battlefield and not isinstance(card,Land) :
            all_creature=list(opponent.battlefield+player.battlefield)
            for i in range(3):
                player.action_store.start_record()
                if all_creature:
                    random_card=random.choice(all_creature)
                    self.proliferate(random_card)
                    all_creature.remove(random_card)
                    if random_card.player==opponent and random_card.buffs:
                        await self.attact_to_object(opponent,2,"rgba(0,100,0,0.5)","Missile_Hit")
            for i in range(3):
                player.action_store.end_record()
        
    def proliferate(self,card:Card):
        store=[]
        for buff in list(card.buffs):
            if not (buff.content in store):
                new_buff=type(buff)(**buff.init_params)
                card.gain_buff(new_buff,self)
                store.append(buff.content)
        
        
            
        