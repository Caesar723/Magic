from pathlib import Path

import onnxruntime as ort
import torch
import torch.nn.functional as F

from game.game_function_tool import ORGPATH
from game.rlearning.onnx_export.torch_session import TorchONNXSession
from game.rlearning.utils.baseAgent import BaseTrainer



class CASTER_PPO_Pointer(BaseTrainer):
    def __init__(self, config,restore_step, rank=0, n_gpus=1,name="main"):
        super().__init__(config,restore_step, rank, n_gpus,name)
    def _init_extra(self):
        super()._init_extra()

        config=self.config["extra"]["onnx"]
        root=Path(ORGPATH).resolve().parent
        device=torch.device(f"cuda:{self.rank}" if torch.cuda.is_available() else "cpu")

        self.extra={
            "device":device,
            "action_embedding":TorchONNXSession(
                root/config["action_embedding"]["path"],
                device,
                config["providers"]
            ),
            "card_embedding":TorchONNXSession(
                root/config["card_embedding"]["path"],
                device,
                config["providers"]
            )
        }
    def _forward(self, batch, models, isTrain, step, epoch):
        batch=self.predict(batch,models,isTrain,step,epoch)
        total_loss=0

        loss={}

        if self.config.get("w_val_loss",0)>0:
            val_loss=F.mse_loss(batch["rewards_adv"].detach(),batch["value"])
            total_loss+=self.config["w_val_loss"]*val_loss
            loss["val_loss"]=val_loss

        if self.config.get("w_act_loss",0)>0:
            
            rate=torch.exp(batch["new_prob_log"]-batch["old_prob_log"].detach()).unsqueeze(1)

            adv = batch["advantage"].detach()
            surr1=rate*adv
            surr2=torch.clamp(rate,1-self.config["ppo"]["clip_para"],1+self.config["ppo"]["clip_para"])*adv
            
            act_loss=-torch.min(surr1,surr2).squeeze(1)#-0.01*batch["entropy"]
            act_loss=act_loss.mean()

            total_loss+=self.config["w_act_loss"]*act_loss
            loss["act_loss"]=act_loss

        if self.config.get("w_kl_loss",0)>0:
            old_dist=torch.distributions.Categorical(batch["old_actions"])
            kl_per_state = torch.distributions.kl.kl_divergence(old_dist, batch["dist"])
            #print(kl_per_state,kl_per_state.shape)
            kl_loss=kl_per_state.mean()
            total_loss+=self.config["w_kl_loss"]*kl_loss
            loss["kl_loss"]=kl_loss

        if self.config.get("w_entropy_loss",0)>0:

            entropy_loss=-batch["entropy"]
            entropy_loss=entropy_loss.mean()
            total_loss+=self.config["w_entropy_loss"]*entropy_loss
            loss["entropy_loss"]=entropy_loss

        
        return batch, loss

    def predict(self, batch, models, isTrain, step, epoch):
        return batch