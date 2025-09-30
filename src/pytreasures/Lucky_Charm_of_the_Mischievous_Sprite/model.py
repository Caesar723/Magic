
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
import random
from game.treasure import Treasure

from game.buffs import KeyBuff,StateBuff,Indestructible,Buff
from game.type_cards.creature import Creature


class Summon_Die_Tree(Buff):
    def __init__(self,card:"Card",selected_card:"Card") -> None:
        super().__init__(card,selected_card)
        self.card=card#这个buff是属于哪一张卡的
        self.content:str="Summon one 1/1 tree"#描述buff
        self.buff_name=f"{card.name}"

    def change_function(self,card:"Creature"):
        previews_func=card.when_die
        async def when_die(self_card,player,opponent):
            await previews_func(player,opponent)
            creature_tree=Small_Tree_Man(card.player)
            player.append_card(creature_tree,"battlefield")
        card.when_die = types.MethodType(when_die, card)

class Small_Tree_Man(Creature):
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Tree man"
        self.live:int=1
        self.power:int=1
        self.actual_live:int=1
        self.actual_power:int=1

        self.type_creature:str="Creature"
        self.type:str="Creature"

        self.mana_cost:str="1"
        self.color:str="green"
        self.type_card:str="Creature"
        self.rarity:str="Uncommon"
        self.content:str=""
        self.image_path:str="cards/creature/Thornwood Sentinel/image.jpg"
    

class Lucky_Charm_of_the_Mischievous_Sprite(Treasure):
    name="Lucky Charm of the Mischievous Sprite"
    content="At the start of your turn, add a random beneficial effect to your random creature in your hand."
    price=22
    background="Crafted by mischievous sprites, this charm brings luck to those who bear it."
    image_path="treasures/Lucky_Charm_of_the_Mischievous_Sprite/image.png"

    def change_function(self,player:"Player"):
        
        previews_func=player.beginning_phase
        async def beginning_phase(self_player):
            result=await previews_func()
            if player.hand:
                cards=player.get_cards_by_pos_type("hand",(Creature,))
                if cards:
                    random_card=random.choice(cards)
                    buff=self.get_random_buff(random_card)
                    random_card.gain_buff(buff,random_card)
            return result
        player.beginning_phase = types.MethodType(beginning_phase, player)

    def get_random_buff(self,card):
        percent=random.randint(0,100)
        if percent<25:
            return StateBuff(self,card,random.randint(1,3),random.randint(1,3))
        elif percent<50:
            return Indestructible(self,card)

            
        elif percent<75:
            key_words=["lifelink","flying","Trample","haste","Vigilance","Double strike","Menace","Hexproof"]
            key_word=random.choice(key_words)
            return KeyBuff(self,card,key_word)

        return Summon_Die_Tree(self,card)


