import sys
if __name__=="__main__":

    from pathlib import Path
    src_root = next(parent for parent in Path(__file__).resolve().parents if parent.name == "src")
    if str(src_root) not in sys.path:
        sys.path.append(str(src_root))
    
from typing import TYPE_CHECKING
import torch


from game.rlearning.inference.protocol import PolicyUpdate
from game.rlearning.utils.data import batch_to_cuda
from initinal_file import ORGPATH,CARD_SIMULATION_DICTION
from game.rlearning.utils.baseParallelEnv import BaseParallelEnv
if TYPE_CHECKING:
    from game.rlearning.communicate.training_parallel_room import Info_Communication


class Parallel_Env(BaseParallelEnv):
    

    def run(self):

        if self.env_config.get("test_mode",False):
            self.collect_test_data()
            return

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
            
    def collect_test_data(self):
        datas={}
        number=self.env_config["test_samples_per_scene"]

        for name in self.env_config["test_cards"]:
            simulation=CARD_SIMULATION_DICTION[name]
            for func in simulation.get_candidates_simulation(simulation):
                datas[name,func.__name__]=[]

        while any(len(items)<number for items in datas.values()):
            batch=self.info_communication.get_game_data()
            for data in batch:
                card=data["state"]["card_used"]
                key=(card["card_key"],card["scenario"])
                if len(datas[key])<number:
                    datas[key].append(data)

        result={
            "env_config":self.env_config,
            "agent_config":self.config,
            "datas":datas,
        }
        with open(self.env_config["test_output"],"xb") as file:
            torch.save(result,file)
                


    def evaluate_test_batch(self,batch):
        trainer=self.agent1
        batch=batch_to_cuda(batch,trainer.rank)

        for model in trainer.models.values():
            model.eval()

        with torch.no_grad():
            batch=trainer.encode(batch,trainer.models,False,trainer.step,trainer.epoch)
            selection=torch.arange(batch["mean_p"].shape[0],device=batch["mean_p"].device)
            views=trainer._synthesis_decoder_predictions(trainer.models,batch,selection)
            return views["prior"]["prediction"]
