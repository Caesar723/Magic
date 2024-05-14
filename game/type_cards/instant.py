from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player




from game.card import Card
from game.type_action import actions
from game.game_function_tool import select_object



class Instant(Card):
    
    def __init__(self,player) -> None:
        super().__init__(player)

    @select_object("",1)
    def card_ability(self,player:'Player'=None,opponent:'Player'=None,selected_object:tuple['Card']=()):
        pass

    def calculate_spell_power(self):
        pass

    def when_select_target(self):
        pass

    async def when_play_this_card(self,player:'Player'=None,opponent:'Player'=None):# when player use the card
        await super().when_play_this_card(player, opponent)

        player.remove_card(self,"hand")

        prepared_function=await self.card_ability(player,opponent)
        
        return prepared_function
    
    def text(self,player)-> str:
        Flying=0
        Active=0
        Player=self.player.text(player)
        Id=id(self)
        Name=self.name
        Type=self.color
        Type_card=self.type_card
        Rarity=self.rarity
        Content=self.content
        Image_Path=self.image_path
        Fee=self.mana_cost
        
        return f"Instant({Flying},{Active},{Player},int({Id}),string({Name}),{Type},{Type_card},{Rarity},string({Content}),{Image_Path},{Fee})"

    def __repr__(self):
        content=f"({self.name},{self.type},{id(self)},{self.mana_cost})"
        return content