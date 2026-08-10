import sys
if __name__=="__main__":

    from pathlib import Path
    src_root = next(parent for parent in Path(__file__).resolve().parents if parent.name == "src")
    if str(src_root) not in sys.path:
        sys.path.append(str(src_root))
    
from typing import TYPE_CHECKING


from game.rlearning.inference.protocol import PolicyUpdate
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
                if self.inference_communication is not None:
                    self.inference_communication.control_queue.put(PolicyUpdate(
                        policy_id="main",
                        config_path=self.config_path,
                        restore_step=-1,
                    ))

            if self.agent1.step >= self.agent1.total_step:  
                if self.agent1.rank == 0:
                    self.agent1.save_checkpoint() 
                self.stop_inference_server()
                return 
            
            



