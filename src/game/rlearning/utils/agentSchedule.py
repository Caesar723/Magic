import random
import os

class AgentSchedule:
    items = ["good_model.txt", "great_model.txt"]
    probs = [0.3, 0.7] 

    paths_cache={

    }
    

    @classmethod
    def get_restore_step(cls,agent):
        logdir=agent.agent.logdir
        item=random.choices(cls.items, cls.probs, k=1)[0]
        #print(os.path.join(logdir, item))
        item_path=os.path.join(logdir, item)
        if item_path in cls.paths_cache:
            return random.choice(cls.paths_cache[item_path])
        if os.path.exists(item_path):
            with open(item_path, "r") as f:
                paths=f.read().split("\n")
                paths.pop()
                cls.paths_cache[item_path]=paths
                random_restore=random.choice(paths)
                #print(random_restore)
                return random_restore
        else:
            paths=[path.split("_")[1].split(".")[0] for path in os.listdir(os.path.join(logdir,"ckpt")) if path.startswith("config")]
            random_restore=random.choice(paths)
            return random_restore