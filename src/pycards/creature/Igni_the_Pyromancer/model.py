
from __future__ import annotations
from typing import TYPE_CHECKING,Union
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
import random
from game.type_cards.creature import Creature
from game.type_cards.sorcery import Sorcery
from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object


class Igni_the_Pyromancer(Creature):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Igni the Pyromancer"
        self.live:int=2
        self.power:int=2
        self.actual_live:int=2
        self.actual_power:int=2

        self.type_creature:str="Human Shaman"
        self.type:str="Creature"

        self.mana_cost:str="2R"
        self.color:str="red"
        self.type_card:str="Human Shaman"
        self.rarity:str="Rare"
        self.content:str="Whenever Igni the Pyromancer deals damage to a player, you randomly cast an instant or sorcery spell from your graveyard without paying its mana cost."
        self.image_path:str="cards/creature/Igni the Pyromancer/image.jpg"

    async def when_harm_is_done(self,card:Union["Creature","Player"],value:int,player: "Player" = None, opponent: "Player" = None):#当造成伤害时 OK
        result= await super().when_harm_is_done(card,value,player,opponent)
        
        if isinstance(card,type(player)) or isinstance(card,type(opponent)):
            cards=player.get_cards_by_pos_type("graveyard",(Instant,Sorcery),except_type=(Instant_Undo,))
            if cards:
                card:"Instant|Sorcery"=random.choice(cards)
                print(card)
                prepared_function=await card.card_ability(player,opponent,selected_object=(card,),selection_random=True,auto_select=True)
                await prepared_function()
        return result

        