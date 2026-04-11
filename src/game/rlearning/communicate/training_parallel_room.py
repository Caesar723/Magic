from torch.multiprocessing import Queue
from queue import Full, Empty
import random
from initinal_file import ORGPATH


class Info_Communication:
    def __init__(self,env_config,manager):
        self.data_queue = Queue(maxsize=20)
        self.num_worker = env_config["num_worker"]
        self.communication={key:manager.dict() for key in range(self.num_worker)}
        self.config_path_list=[f"{ORGPATH}/{config_path}" for config_path in env_config["opponent_config"]]

        self.update_model(0,0)
        for i in range(self.num_worker):
            self.update_model_opponent(i,random.choice(self.config_path_list),0)

    def store_game_data(self,data:list[dict]):
        try:
            self.data_queue.put(data, block=False)
        except Full:
            try:
                self.data_queue.get(block=False)
            except Empty:
                pass
            self.data_queue.put(data, block=False)

    def get_game_data(self):
        return self.data_queue.get()


    def check_model_update(self,worker_id:int):
        return self.communication[worker_id].get("model_update",False)
            
    def get_model_info(self,worker_id:int):

        result={
            
            "success_update":self.communication[worker_id].get("model_update",False),
            "model_update_steps":self.communication[worker_id].get("model_update_steps",0),
            "model_path":self.communication[worker_id].get("model_path",None),

            "success_opponent_update":self.communication[worker_id].get("model_opponent_update",False),
            "config_opponent_path":self.communication[worker_id].get("config_opponent_path",None),
            "model_opponent_path":self.communication[worker_id].get("model_opponent_path",None),
        }
        self.communication[worker_id]["model_update"]=False
        self.communication[worker_id]["model_opponent_update"]=False
        return result


    def update_model(self,steps,model_path:str):
        for worker_id in range(self.num_worker):
            self.communication[worker_id]["model_update"]=True
            self.communication[worker_id]["model_update_steps"]=steps
            self.communication[worker_id]["model_path"]=model_path

    def update_model_opponent(self,worker_id:int,config_opponent_path:str,model_path:str):
        self.communication[worker_id]["model_opponent_update"]=True
        self.communication[worker_id]["config_opponent_path"]=config_opponent_path
        self.communication[worker_id]["model_opponent_path"]=model_path
