import sys
if __name__=="__main__":

    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/src")
    
from typing import TYPE_CHECKING
import random


from initinal_file import ORGPATH
from game.rlearning.utils.common import CHECKPOINT_ROOT_PATH
from game.rlearning.utils.model import get_class_by_name
from game.rlearning.utils.file import read_yaml
from game.rlearning.utils.baseParallelEnv import BaseParallelEnv
from game.rlearning.utils.agentSchedule import AgentSchedule
if TYPE_CHECKING:
    from game.rlearning.communicate.training_parallel_room import Info_Communication


class Parallel_Env(BaseParallelEnv):
    

    def initinal_config(self,config:dict):
        super().initinal_config(config)

        
        config_path_list=[f"{ORGPATH}/{config_path}" for config_path in config["opponent_config"]]
        self.config_list={
            config_path:read_yaml(config_path) for config_path in config_path_list}
        
    def run(self):


        while True:
            data=self.info_communication.get_game_data()
            self.agent1.store_round_data(data)

            is_update=self.agent1.update()
            if is_update:
                self.info_communication.update_model(self.agent1.step,-1)
                
            for worker_id in range(self.num_worker):
                if not self.info_communication.check_model_update(worker_id):
                    agent_path,config=random.choice(list(self.config_list.items()))
                    
                    logdir=f"{ORGPATH}/../{CHECKPOINT_ROOT_PATH}/{config['log_dir']}"
                    restore_step=AgentSchedule.get_restore_step(logdir)
                    print(agent_path,restore_step)
                    self.info_communication.update_model_opponent(worker_id,agent_path,restore_step)

            if self.agent1.step >= self.agent1.total_step:  
                if self.agent1.rank == 0:
                    self.agent1.save_checkpoint() 
                return 

