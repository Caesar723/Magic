
import torch
import torch.nn.functional as F


from game.rlearning.utils.baseAgent import BaseTrainer



class AgentTestTrainer(BaseTrainer):
    def __init__(self, config,restore_step, rank=0, n_gpus=1,name="main"):
        super().__init__(config,restore_step, rank, n_gpus,name)

    @torch.no_grad()
    def choose_action(self,batch,extra_keys=[],isTrain=False):#如果是一个动作记得加[batch]

        #print(batch)
        batch=batch[0]

        if "mask" in batch:
            mask=batch["mask"]
        else:
            mask=None

        batch["actions"]=torch.randint(0, 2, (1, 352)).float()

        actions=batch["actions"]

        if mask is not None:
            #print(7)
            actions[mask==False]=0
        
        batch["action"]=torch.argmax(actions)

        return batch
    
    