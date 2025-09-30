
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure
import random



class Mirror_of_Misdirection(Treasure):
    name="Mirror of Misdirection"
    content="Whenever your opponent targets a friendly minion with a spell or effect, there are 30% chance that redirect it to a different random target."
    price=0
    background="Crafted by mischievous gnomes, this enchanted mirror confounds even the most skilled spellcasters."
    image_path="treasures/Mirror_of_Misdirection/image.png"

    def change_function(self,player:"Player"):
        previews_func=player.opponent.receive_text
        async def receive_text(self_player):
            result=await previews_func()
            
            if random.random()<1 and result:
                parameters=result.split("|")
                
                if parameters[1]=="field" and parameters[2]=="opponent_battlefield":
                    
                    if random.random()<0.5:
                        target_self=random.randint(0,len(player.opponent.battlefield)-1)
                        
                        result=[parameters[0],parameters[1],"self_battlefield",str(target_self)]
                        
                    else:
                        target_oppo=random.randint(0,len(player.battlefield)-1)
                        
                        result=[parameters[0],parameters[1],"opponent_battlefield",str(target_oppo)]
                        
                    result='|'.join(result)
                    
            
            return result
        player.opponent.receive_text = types.MethodType(receive_text, player.opponent)
