
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object


class Oblivion_Devourer(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Oblivion Devourer"
        self.live:int=6
        self.power:int=6
        self.actual_live:int=6
        self.actual_power:int=6

        self.type_creature:str="Eldrazi Creature - Eldrazi"
        self.type:str="Creature"

        self.mana_cost:str="5BB"
        self.color:str="black"
        self.type_card:str="Eldrazi Creature - Eldrazi"
        self.rarity:str="Rare"
        self.content:str="Menace (This creature can't be blocked except by two or more creatures), When Oblivion Devourer attacks, you may sacrifice another minimum state creature. If you do, target player discards two cards."
        self.image_path:str="cards/creature/Oblivion Devourer/image.jpg"

        self.flag_dict["Menace"]=True

    async def when_start_attcak(self, card: 'Creature | Player', player: 'Player' = None, opponent: 'Player' = None):
        result= await super().when_start_attcak(card, player, opponent)
        min_state_creature=False
        min_state=999
        for creature in player.battlefield:
            power,life=creature.state
            state=power+life
            if state<min_state and creature!=self:
                min_state=state
                min_state_creature=creature
        if min_state_creature:
            await self.destroy_object(min_state_creature,"rgba(0,0,0,0.8)","Cure")
            
            for i in range(2):
                if opponent.hand:
                    card_hand=random.choice(opponent.hand)
                    opponent.discard(card_hand)


        return result
        