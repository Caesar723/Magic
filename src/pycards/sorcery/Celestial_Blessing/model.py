
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.buffs import KeyBuff


class Celestial_Blessing(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.fixed_id:int=191

        self.name:str="Celestial Blessing"

        self.type:str="Sorcery"

        self.mana_cost:str="1WW"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Choose one target creatures you control and another target creatures nearby. They gain lifelink until end of turn."
        self.image_path:str="cards/sorcery/Celestial Blessing/image.jpg"

    @select_object("your_creatures",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        targets=[]
        if selected_object:
            targets.append(selected_object[0])

        index_target=player.battlefield.index(selected_object[0])
        for i in range(len(player.battlefield)):
            if abs(i-index_target)==1 and not player.battlefield[i].get_flag("tap"):
                targets.append(player.battlefield[i])
            if len(targets)>=2:
                break
        for target in targets:
            buff=KeyBuff(self,target,"lifelink")
            buff.set_end_of_turn()
            target.gain_buff(buff,self)

