
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card

from game.treasure import Treasure
from game.type_cards.creature import Creature
from game.type_cards.sorcery import Sorcery
from game.type_cards.instant import Instant
from game.game_function_tool import select_object
import random

class Lucky_Charm_Card_Creature(Creature):
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Lucky Charm Card"
        self.live:int=2
        self.power:int=1
        self.actual_live:int=2
        self.actual_power:int=1

        self.type_creature:str="Creature"
        self.type:str="Creature"

        self.mana_cost:str="1"
        self.color:str="green"
        self.type_card:str="Creature"
        self.rarity:str="Uncommon"
        self.content:str=""
        self.image_path:str="treasures/Lucky_Clover_Pin/image.png"
    
class Lucky_Charm_Card_Sorcery(Sorcery):
    def __init__(self,player) -> None:
        super().__init__(player)
        self.name:str="Lucky Charm Card"
        self.mana_cost:str="1"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.type:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Draw a card."
        self.image_path:str="treasures/Lucky_Clover_Pin/image.png"
    

    @select_object("",1)
    async def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        player.draw_card(1)

class Lucky_Charm_Card_Instant(Instant):
    def __init__(self,player) -> None:
        super().__init__(player)
        self.name:str="Lucky Charm Card"
        self.mana_cost:str="1"
        self.color:str="green"
        self.type_card:str="Instant"
        self.type:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Deal 1 damage to an object."
        self.image_path:str="treasures/Lucky_Clover_Pin/image.png"
    
    @select_object("all_roles",1)
    async def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        if selected_object:
            player.action_store.start_record()
            await self.attact_to_object(selected_object[0],1,"rgba(0,0,0,0.5)","Missile_Hit")
            player.action_store.end_record()

class Lucky_Clover_Pin(Treasure):
    name="Lucky Clover Pin"
    content="At the start of your turn, add a random Lucky Charm card to your hand."
    price=30
    background="A small, enchanted pin that brings luck and charms to those who wear it."
    image_path="treasures/Lucky_Clover_Pin/image.png"

    def change_function(self,player:"Player"):
        
        if hasattr(player, "id_dict"):
            #print("Lucky_Clover_Pin",player.id_dict)
            max_id=max(player.id_dict.values())
            obj_creature=Lucky_Charm_Card_Creature(player)
            obj_sorcery=Lucky_Charm_Card_Sorcery(player)
            obj_instant=Lucky_Charm_Card_Instant(player)

            player.id_dict[f"{obj_creature.name}+{obj_creature.type}"]=max_id+1
            player.id_dict[f"{obj_sorcery.name}+{obj_sorcery.type}"]=max_id+2
            player.id_dict[f"{obj_instant.name}+{obj_instant.type}"]=max_id+3
            #print("Lucky_Clover_Pin",player.id_dict)
        previews_func=player.beginning_phase

        card_class_list=[Lucky_Charm_Card_Creature,Lucky_Charm_Card_Sorcery,Lucky_Charm_Card_Instant]
        async def beginning_phase(self_player):
            result=await previews_func()
            player.action_store.start_record()
            player.append_card(random.choice(card_class_list)(player),"hand")
            player.action_store.end_record()
            return result
        player.beginning_phase = types.MethodType(beginning_phase, player)
