
from __future__ import annotations
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant,Instant_Undo
from game.game_function_tool import select_object
from game.buffs import Buff
from game.type_cards.creature import Creature


class Witch_s_Curse_Counter_Buff(Buff):
    def __init__(self,card:"Card",selected_card:"Card") -> None:
        super().__init__(card,selected_card)
        self.card=card#这个buff是属于哪一张卡的
        self.card_type:str="State"#这个buff是用在那个类型的
        self.content:str="Reducing strength and stamina by half"#描述buff
        self.buff_name=f"{card.name}"

        self.turn_counter=0
        self.set_end_of_turn()

    def change_function(self,card:"Creature"):
        previews_func=card.calculate_state
        def calculate_state(self_card):
            power,live=previews_func()
            power=round(power/2)
            live=round(live/2)
            return (power,live)
        card.calculate_state = types.MethodType(calculate_state, card)

    def when_end_turn(self):
        self.turn_counter+=1
        if self.turn_counter>=3:
            self.selected_card.loss_buff(self,self.card)
            self.selected_card.player.remove_card_from_dict("end_step_buff",self)


class Witch_s_Curse_Counter(Instant_Undo):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Witch's Curse Counter"

        self.type:str="Instant"

        self.mana_cost:str="2B"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell. Then, its controller's creatures gains a curse for three turns, reducing their strength and stamina by half."
        self.image_path:str="cards/Instant/Witch's Curse Counter/image.jpg"


    @select_object("",1)
    async def card_ability(self, player: "Player", opponent: "Player", selected_object: tuple["Card"]):
        func,card=await self.undo_stack(player,opponent)
        for creature in opponent.battlefield:
            buff=Witch_s_Curse_Counter_Buff(self,creature)
            creature.gain_buff(buff,self)
