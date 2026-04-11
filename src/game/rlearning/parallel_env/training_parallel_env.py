import sys
if __name__=="__main__":

    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/src")
    
from typing import TYPE_CHECKING



from initinal_file import ORGPATH
from game.rlearning.utils.baseParallelEnv import BaseParallelEnv
if TYPE_CHECKING:
    from game.rlearning.communicate.training_parallel_room import Info_Communication


class Parallel_Env(BaseParallelEnv):
    

    def run(self):


        while True:
            data=self.info_communication.get_game_data()
            self.agent1.store_round_data(data)

            is_update=self.agent1.update()
            if is_update:
                self.info_communication.update_model(self.agent1.step,-1)



