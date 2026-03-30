
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant
from game.game_function_tool import select_object


class Ethereal_Reversal(Instant):
    
    
    def __init__(self,player) -> None:
        super().__init__(player)

        self.name:str="Ethereal Reversal"

        self.type:str="Instant"

        self.mana_cost:str="1UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Return target nonland permanent to its owner's hand. You may cast a spell with converted mana cost equal to or less than the returned card's from your hand without paying its mana cost."
        self.image_path:str="cards/Instant/Ethereal Reversal/image.jpg"

    @select_object("all_creatures",1)
    async def card_ability(self,player:"Player"=None,opponent:"Player"=None,selected_object:tuple["Card"] = ()):
        bounced_mv=0
        if selected_object:
            target=selected_object[0]
            if hasattr(target,"type") and target.type!="Land":
                owner=target.player
                if target in owner.battlefield:
                    owner.remove_card(target,"battlefield")
                    owner.append_card(type(target)(owner),"hand")
                bounced_mv=sum(target.cost.values())
        if bounced_mv<=0:
            return
        playable=[c for c in list(player.hand) if c!=self and sum(c.cost.values())<=bounced_mv and c.type in ("Instant","Sorcery")]
        if playable:
            await player.auto_play_card(playable[0],start_bullet_time=False)

