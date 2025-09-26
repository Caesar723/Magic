from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.card import Card
    from game.player import Player


class Treasure:
    
    
    name=""
    content=""
    price=0
    background=""
    image_path=""

    def change_function(self,player:"Player"):
        pass