
from __future__ import annotations
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
import inspect

from game.type_cards.sorcery import Sorcery
from game.game_function_tool import select_object
from game.buffs import Buff 
from game.type_cards.creature import Creature


class Soul_Transfer_buff(Buff):
    def __init__(self,card:"Card",selected_card:"Card",target_cards:list["Card"]) -> None:
        super().__init__(card,selected_card)
        self.card=card#这个buff是属于哪一张卡的
        self.content:str="Gains all die abilities of creature cards in your graveyard"#描述buff
        self.buff_name=f"{card.name}"

        self.target_cards=target_cards

        self.init_params.update({
            "target_cards": target_cards,
        })

    def change_function(self,card:"Creature"):
        previews_func=card.when_die
        async def when_die(self_card,player,opponent):
            await previews_func(player,opponent)
            for target_card in self.target_cards:
                await type(target_card).when_die(self_card,player,opponent)
            
        card.when_die = types.MethodType(when_die, card)


class Soul_Transfer(Sorcery):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Soul Transfer"

        self.type:str="Sorcery"

        self.mana_cost:str="4BB"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Choose one creature. That creature gains all die abilities of creature cards in your graveyard"
        self.image_path:str="cards/sorcery/Soul Transfer/image.jpg"

    @select_object("all_creatures",1)
    async def card_ability(self, player: "Player", opponent: "Player", selected_object: tuple["Card"]=()):
        if selected_object:
            org_func=Creature.when_die
            die_objs=[]
            for card in player.graveyard:
                if isinstance(card,Creature) and\
                inspect.getsource(org_func) != inspect.getsource(type(card).when_die):
                    die_objs.append(card)
            new_buff=Soul_Transfer_buff(self,card,die_objs)
            selected_object[0].gain_buff(new_buff,self)

