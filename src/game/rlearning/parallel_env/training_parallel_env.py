import sys
if __name__=="__main__":

    from pathlib import Path
    src_root = next(parent for parent in Path(__file__).resolve().parents if parent.name == "src")
    if str(src_root) not in sys.path:
        sys.path.append(str(src_root))
    
from typing import TYPE_CHECKING
import random


from initinal_file import ORGPATH
import game.rlearning.utils.log as log
from game.rlearning.utils.common import CHECKPOINT_ROOT_PATH
from game.rlearning.utils.model import get_class_by_name
from game.rlearning.utils.file import read_yaml
from game.rlearning.utils.baseParallelEnv import BaseParallelEnv
from game.rlearning.utils.agentSchedule import AgentSchedule
from game.rlearning.inference.protocol import PolicyUpdate
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
                if self.inference_communication is not None:
                    self.inference_communication.control_queue.put(PolicyUpdate(
                        policy_id="main",
                        config_path=self.config_path,
                        restore_step=-1,
                    ))
            if self.evaluator is not None:
                report = self.evaluator.poll_evaluation()

                if report is not None:
                    self.log_evaluation(report)

                interval = int(self.env_config.get("evaluation_interval", 10000))

                if (
                    is_update
                    and self.evaluator.active is None
                    and self.agent1.step - self.last_evaluation_step >= interval
                ):
                    self.agent1.save_checkpoint()

                    self.evaluator.start_evaluation(self.agent1.step)

                    self.last_evaluation_step = self.agent1.step
                            
            for worker_id in range(self.num_worker):
                if not self.info_communication.check_model_update(worker_id):
                    agent_path,config=random.choice(list(self.config_list.items()))
                    
                    logdir=f"{CHECKPOINT_ROOT_PATH}/{config['log_dir']}"
                    restore_step=AgentSchedule.get_restore_step(logdir)
                    #print(agent_path,restore_step)
                    self.info_communication.update_model_opponent(worker_id,agent_path,restore_step)

            if self.agent1.step >= self.agent1.total_step:  
                if self.agent1.rank == 0:
                    self.agent1.save_checkpoint() 
                self.stop_inference_server()
                return 

    def log_evaluation(self, report):
        step = report["step"]

        prefix = f"evaluation/{report['benchmark_id']}"

        if report["score"] is not None:
            log.sw_scalar(f"{prefix}/score", report["score"], step)

        # log.sw_scalar(f"{prefix}/valid", int(report["valid"]), step)

        # for name in ("games", "completed", "truncated", "errors"):
        #     log.sw_scalar(f"{prefix}/{name}", report[name], step)

        if log.SW is not None:
            log.SW.flush()

    def start_worker(self):
        self.evaluator = None
        self.last_evaluation_step = self.agent1.step
        super().start_worker()
        path = self.env_config.get("evaluation_config")
        if path is None:
            return
        config = read_yaml(f"{ORGPATH}/{path}")
        self.evaluator = get_class_by_name(config["env"])(config, agent_config=self.env_config["agent_config"])
        self.evaluator.start_worker()
