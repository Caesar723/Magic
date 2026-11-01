import asyncio
from pathlib import Path
from game.rlearning.utils.common import CHECKPOINT_ROOT_PATH


class PveAgent:
    def __init__(self,config_path:str,config:dict,inference):
        self.config_path=str(Path(config_path).expanduser().resolve(strict=True))
        self.config=config
        self.inference=inference
        self.restore_step=config["restore_step"]
        self.name="pve"
        self.logdir=f"{CHECKPOINT_ROOT_PATH}/{config['log_dir']}"
        self.step=self.numeric_step(self.restore_step)
        self.rollout_state_fields=config.get("rollout_state_fields",{})
        self.lock=asyncio.Lock()
        self.reset_rollout_context()

    @staticmethod
    def numeric_step(value):
        try:
            return max(0,int(value))
        except (TypeError,ValueError):
            return 0

    def reset_rollout_context(self):
        self.rollout_context={key:None for key in self.rollout_state_fields}

    def choose_action(self,batch,extra_keys=None,isTrain=False):
        raise RuntimeError("PveAgent requires choose_action_async()")

    async def choose_action_async(self,state:dict):
        async with self.lock:
            payload=dict(state)
            payload.update(self.rollout_context)

            result=await self.inference.choose_action(self.config_path,self.restore_step,payload)
            next_context={key:result[name] for key,name in self.rollout_state_fields.items()}

            self.rollout_context=next_context
            return result