
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Sacred_Reinforcement(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)
        self.effect_params:dict={"power_bonus":1,"toughness_bonus":1}

        self.fixed_id:int=61

        self.name:str="Sacred Reinforcement"

        self.type:str="Instant"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Tap target creature. It gains +{power_bonus}/+{toughness_bonus} until end of turn."
        self.image_path:str="cards/Instant/Sacred Reinforcement/image.jpg"

    @select_object("opponent_creatures",1)
    async def card_ability(self, player: "Player" = None, opponent: "Player" = None, selected_object: tuple["Card"] = ...):
        from game.buffs import Tap, StateBuff
        
        for target in selected_object:
            buff_tap = Tap(self, target)
            target.gain_buff(buff_tap, self)
            
            buff_stats = StateBuff(self, target, self.effect_params["power_bonus"], self.effect_params["toughness_bonus"])
            buff_stats.set_end_of_turn()
            target.gain_buff(buff_stats, self)




        