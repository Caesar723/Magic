
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.creature import Creature
from game.game_function_tool import select_object
from game.type_cards.sorcery import Sorcery
from game.type_cards.instant import Instant,Instant_Undo
from game.type_action.actions import Play_Cards

class Temporal_Traveler(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Temporal Traveler"
        self.live:int=4
        self.power:int=3
        self.actual_live:int=4
        self.actual_power:int=3

        self.type_creature:str="Creature - Wizard"
        self.type:str="Creature"

        self.mana_cost:str="4UU"
        self.color:str="blue"
        self.type_card:str="Creature - Wizard"
        self.rarity:str="Rare"
        self.content:str="Whenever Temporal Traveler attacks, you may cast an instant or sorcery card from your graveyard without paying its mana cost."
        self.image_path:str="cards/creature/Temporal Traveler/image.jpg"

    async def when_start_attcak(self, card: "Creature | Player", player: "Player" = None, opponent: "Player" = None):
        
        cards_graveyard=player.get_cards_by_pos_type("graveyard",(Instant,Sorcery),except_type=(Instant_Undo,))
        if cards_graveyard:
            card_graveyard:"Instant|Sorcery"=random.choice(cards_graveyard)
            
            new_func=await card_graveyard.card_ability(player,opponent,auto_select=True)
            #await player.room.put_prepared_function_to_stack(new_func,card_graveyard)
            player.room.action_processor.start_record()
            player.room.action_processor.start_record()
            player.room.action_processor.add_action(Play_Cards(card_graveyard,card_graveyard.player))
            player.room.action_processor.end_record()
            
            await new_func()
            player.room.action_processor.end_record()

        