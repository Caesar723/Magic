import sys
if __name__=="__main__":

    from pathlib import Path
    src_root = next(parent for parent in Path(__file__).resolve().parents if parent.name == "src")
    if str(src_root) not in sys.path:
        sys.path.append(str(src_root))
    
from typing import TYPE_CHECKING



from initinal_file import ORGPATH
from game.rlearning.utils.baseParallelEnv import BaseParallelEnv
if TYPE_CHECKING:
    from game.rlearning.communicate.training_parallel_room import Info_Communication


class Parallel_Env(BaseParallelEnv):
    

    def run(self):


        while True:
            
            data=self.info_communication.get_game_data()
            #self.agent1.store_round_data(data)
            
            print(len(data))
            
            



