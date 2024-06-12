from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player





from game.card import Card
from game.type_action import actions
from game.game_function_tool import select_object


class Sorcery(Card):
    
    def __init__(self,player) -> None:
        super().__init__(player)

    @select_object("",1)
    async def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):# when player use the card
        pass

    def calculate_spell_power(self):
        pass

    def when_select_target(self):
        pass

    async def when_play_this_card(self,
                            player:'Player'=None,
                            opponent:'Player'=None,
                            ):# when player use the card
        await super().when_play_this_card(player, opponent)

        
        prepared_function=await self.card_ability(player,opponent)
        if prepared_function=="cancel":
            return prepared_function
        player.remove_card(self,"hand")
        return prepared_function
    
    def text(self,player:'Player',show_hide:bool=False)-> str:
        Flying=0
        Active=0
        Player=self.player.text(player)
        Id=id(self)
        if show_hide and player.name!=self.player.name:
            return f"Opponent({Player},int({Id}))"
        Name=self.name
        Type=self.color
        Type_card=self.type_card
        Rarity=self.rarity
        Content=self.content
        Image_Path=self.image_path
        Fee=self.mana_cost
        
        return f"Sorcery({Flying},{Active},{Player},int({Id}),string({Name}),{Type},{Type_card},{Rarity},string({Content}),{Image_Path},{Fee})"

    
    def __repr__(self):
        content=f"({self.name},{self.type},{id(self)},{self.mana_cost})"
        return content