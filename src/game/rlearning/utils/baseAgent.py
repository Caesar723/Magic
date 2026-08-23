
import os, random, yaml, tqdm,time, sys
import numpy as np 
import subprocess
from multiprocessing import Process
import threading
import torch 
import torch.nn as nn 




from torch.optim import AdamW 
from torch.optim.lr_scheduler import ExponentialLR, LambdaLR
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.nn.parallel import DataParallel as DP

from game.rlearning.utils.model import get_class_by_name, init_model, whether_contain_parameters
from game.rlearning.utils.file import read_symbol_link, save_yaml, set_symbol_link
import game.rlearning.utils.log as log 
from game.rlearning.utils.data import batch_to_cuda,detach_cuda,to_cpu
from game.rlearning.utils.common import CHECKPOINT_ROOT_PATH
from game.game_function_tool import ORGPATH

def nested_get(d, keys):
    for k in keys:
        if not isinstance(d,dict) or k not in d:
            return None
        d = d[k]
    return d
def _collate_batch(batch, s_keys, g_keys,extra_keys=[]):
    #规定&为字典层级分割符
    
    collate_batch = {}
    #-----------------------
    for k in s_keys:
        k=k.split("&")
        v=nested_get(batch[0],k)
        if v is None:
            continue
        collate_batch["_".join(k)] = [ nested_get(b,k) for b in batch ]

    #-----------------------

    for k in g_keys:
        k=k.split("&")
        v=nested_get(batch[0],k)
        
        
        if v is None:
            continue
        v = [ torch.from_numpy(np.array(nested_get(b,k))) for b in batch ]
        # print([i.shape for i in v])
        for ek in extra_keys:
            if ek in k:
                k.remove(ek)
        collate_batch["_".join(k)] = torch.stack(v, dim=0)
        # print(collate_batch[k].shape)
        # print(k)
    
    return collate_batch
class BaseTrainer:
    def __init__(self, config,restore_step, rank=0, n_gpus=1,name="main"):
        self.config = config
        self.n_gpus = n_gpus 
        self.rank = rank 
        self.name=name

        # random.seed(config["seed"]) 
        # np.random.seed(config["seed"]) 
        # torch.manual_seed(config["seed"])
        # torch.cuda.manual_seed(config["seed"]) 
        if torch.cuda.is_available():
            torch.cuda.init()
            torch.cuda.set_device(rank) 
            #torch.cuda.synchronize()
        

        if self.rank == 0:
            log.info( "Config:\n" + yaml.safe_dump(config) ) 

        #-----------------models------------------
        self.models_config = config["model"] 
        self.models_class = { k: get_class_by_name(cfg["class_name"]) 
                              for k, cfg in config["model"].items() } 
        self.models = dict() 
        self._models = dict() 
        self.models_test = dict()
        self.optims = dict()
        self.g_keys = []
        self.i_keys = []
        for k, cfg in config["model"].items():
            if torch.cuda.is_available():
                model = init_model(cfg).cuda(rank)  
            elif torch.backends.mps.is_available():
                model = init_model(cfg).to(torch.device("mps"))
            else:
                model = init_model(cfg)
            if whether_contain_parameters(model):
                if self.n_gpus > 1:
                    #  DistributedDataParallel
                    #  the batch won't be split, but update in parallel for each gpu, thus faster update frequence
                    model = nn.SyncBatchNorm.convert_sync_batchnorm(model) 
                    model = DDP(model, device_ids=[rank]) 
                    if self.rank == 0: 
                        log.info(f"Using DistributedDataParallel with {self.n_gpus} gpus.")
                if self.n_gpus < -1:
                    #  DataParallel
                    #  the batch will be split in net.forward(), thus larger batch, but same update frequence
                    #  Arbitrary positional and keyword inputs are allowed to be passed into
                    #  DataParallel but some types are specially handled. tensors will be
                    #  **scattered** on dim specified (default 0). tuple, list and dict types will
                    #  be shallow copied. The other types will be shared among different threads
                    #  and can be corrupted if written to in the model's forward pass.
                    model = nn.DataParallel(model)
                    if self.rank == 0: 
                        log.info(f"Using DataParallel with {abs(self.n_gpus)} gpus.")

                if not cfg.get("ignore_optim", False):
                    #to save gpu resources
                    if cfg.get("is_g", True):
                        learning_rate=config["optimizer"]["learning_rate"]
                    else:
                        learning_rate=config["optimizer"].get("learning_rate_d",config["optimizer"]["learning_rate"])
                    self.optims[k] = AdamW( model.parameters(), 
                                        lr=learning_rate, 
                                        betas=config["optimizer"]["betas"],
                                        eps=config["optimizer"]["eps"],
                                        weight_decay=config['optimizer'].get('weight_decay', 1e-2)) 

            if cfg.get("is_g", True):
                self.g_keys.append(k)
            else:
                self.i_keys.append(k)

            self.models[k] = model
            if self.n_gpus > 1:
                self._models[k] = model.module
            elif self.n_gpus < -1:
                self._models[k] = model.module
            else:
                self._models[k] = model
            if torch.cuda.is_available():
                self.models_test[k] = init_model(cfg).cuda(rank) 
            elif torch.backends.mps.is_available():
                self.models_test[k] = init_model(cfg).to(torch.device("mps"))
            else:
                self.models_test[k] = init_model(cfg)
            self.models_test[k].load_state_dict(self._models[k].state_dict())  
            
        
        self.logdir = f'{ORGPATH}/../{CHECKPOINT_ROOT_PATH}/{config["log_dir"]}'
        print(self.logdir)
        if rank == 0: 
            if name=="main":
                log.init(self.logdir)
            for k in self.g_keys:
                log.info( "Network of {}: \n{}".format(k, self.models[k]) ) 
            for k in self.i_keys:
                log.info( "Independent of {}: \n{}".format(k, self.models[k]) ) 
            #log.info( "Config:\n" + yaml.safe_dump(config) ) 

        self.total_step = config["total_step"] 
        self.step = 0 
        self.epoch = 0 

        if self.config["optimizer"]["n_warmup_steps"] < 0:
            self.scheds = { k: ExponentialLR( opt, gamma=self.config["scheduler"]["gamma"]) 
                        for k, opt in self.optims.items() } 
        else:
            warmup_steps = self.config["optimizer"]["n_warmup_steps"] // self.config["scheduler"]["step_size"]
            total_steps  = self.config["total_step"] // self.config["scheduler"]["step_size"]

            def lr_lambda(current_step):
                if current_step < warmup_steps:
                    return float(current_step) / float(max(1, warmup_steps))
                # after warm-up: linearly decay back to 0
                return max(
                    0.0,
                    float(total_steps - current_step) / float(max(1, total_steps - warmup_steps))
                )
            self.scheds = { k: LambdaLR(opt, lr_lambda) for k, opt in self.optims.items() }

        if restore_step != 0:
            self.restore_checkpoint(restore_step) 
        self.max_step=self.step

        self._init_dataset()
        self._init_extra()



        self.embedding_store_data = None


    def _init_dataset(self):
        config = self.config 
        self.dataset_class = get_class_by_name(config["dataset_class_name"])
        dataset = self.dataset_class(config) 
        self.dataset = dataset 

    def _init_dataloader(self):
        config = self.config 
        #self._init_dataset()

        if self.n_gpus > 1:
            sampler = DistributedSampler(self.dataset, self.n_gpus, self.rank, drop_last=True, shuffle=True) 
            self.dataloader = DataLoader(self.dataset, 
                                batch_size=config["dataloader"]["batch_size"], 
                                collate_fn=self.dataset.collate_fn, 
                                num_workers=config["dataloader"]["num_workers"], 
                                sampler=sampler) 
        else:
            n_devices = abs(self.n_gpus)
            batch_size = config["dataloader"]["batch_size"] * (n_devices if n_devices else 1)
            if n_devices > 1:
                log.info(f"Update batch size to {batch_size} with {n_devices} gpus.")
            self.dataloader = DataLoader(self.dataset, 
                                batch_size=batch_size, 
                                collate_fn=self.dataset.collate_fn, 
                                num_workers=config["dataloader"]["num_workers"],
                                drop_last=True,
                                shuffle=config["dataloader"].get("shuffle",True)) 

    def store(self,data):
        self.dataset.store_data(data)
        # if self.dataset.is_full():
            
        #     self.dataset.data_preprocess(self)
        #     self._init_dataloader()
        #     self.run()
        #     self.dataset.clear_data()

    def store_round_data(self,datas):
        self.dataset.store_round_data(datas)

    def update(self):
        if self.dataset.is_full():
            self.store_embedding_to_tensorboard()

            self.dataset.data_preprocess(self)
            self._init_dataloader()
            self.run()
            # The rollout service loads g_last after this method returns.  Save
            # after optimisation, otherwise it would always receive the model
            # from before the just-finished update.
            self._moving_average()
            self.save_checkpoint()
            self.dataset.clear_data()
            return True
        return False


    def run(self):
        
        models = self.models
        [ models[k].train() for k in models ] 

        print( f"Rank {self.rank}, start training" ) 

        
        train_mode=self.config.get("train_mode",0)
        for _ in range(self.config["n_epoch"]):
            for batch in self.dataloader:

                batch = batch_to_cuda(batch, self.rank)
                
                [self.models[k].requires_grad_(True if train_mode==0 or train_mode==2 else False) for k in self.g_keys]#把g的参数设置为可训练
                [self.models[k].requires_grad_(False) for k in self.i_keys]#把d的参数设置为不可训练
                loss_dict = self._forward(batch, models, isTrain=True, step=self.step, epoch=self.epoch)
                if train_mode==0 or train_mode==2:
                    self._update_g(loss_dict)
                
                batch = detach_cuda(batch)
                [self.models[k].requires_grad_(True if train_mode==0 or train_mode==2 else False) for k in self.i_keys]#把d的参数设置为可训练
                [self.models[k].requires_grad_(False) for k in self.g_keys]#把g的参数设置为不可训练
                loss_dict |=self._forward_independent(batch, models, isTrain=True, step=self.step, epoch=self.epoch)
                if train_mode==0 or train_mode==2:
                    self._update_independent(loss_dict)


                self.check_log(loss_dict) 
                
                if self.step >= self.total_step:
                   
                    if self.rank == 0:
                        self.save_checkpoint() 
                        log.info("Finish training.") 
                    return 
                
                if self.step % self.config["scheduler"]["step_size"] == 0:
                    [ self.scheds[k].step() for k in self.scheds ] 

                self.step += 1 
            self.epoch += 1




    def restore_checkpoint(self, restore_step):
        if restore_step == 0:
            return

        if restore_step == -1:
            cpg = read_symbol_link(f"{self.logdir}/ckpt/g_last")
            cpd = read_symbol_link(f"{self.logdir}/ckpt/i_last")
        else:
            cpg = f"{self.logdir}/ckpt/g_{restore_step}" 
            cpd = f"{self.logdir}/ckpt/i_{restore_step}"
        if not os.path.isfile(cpg): 
            raise ValueError(f"Not find checkpoint for {restore_step} step") 
        
        state_dict = {} 
        state_dict.update( torch.load(cpg, weights_only=True, map_location="cpu") )
        if os.path.isfile(cpd):
            print(f"restore i model from {cpd}")
            state_dict.update( torch.load(cpd, weights_only=False, map_location="cpu") ) 

        error_keys = []
        for k in self._models:
            try:
                if self.config["model"][k].get("ignore_state",False):
                    continue
                self._models[k].load_state_dict(state_dict[k], strict=False)
                self.models_test[k].load_state_dict(state_dict[k], strict=False) 
            except:
                if self.rank == 0:
                    log.info(f"error restore model {k}, but continue.")
                error_keys.append(k)
        
        #there might be error if d model is not found, fix later
        if len(error_keys) == 0:
            for k in self.optims:
                try:
                    if self.config["model"][k].get("ignore_state",False):
                        continue
                    self.optims[k].load_state_dict( state_dict["optim"][k]) 
                except:
                    if self.rank == 0:
                        print(f"error restore optims {k}, but continue.")
                    error_keys.append(k)
                    pass
            for k in self.scheds:
                if self.config.get("reset_learning_rate", False):
                    continue
                try:
                    self.scheds[k].load_state_dict( state_dict["scheds"][k]) 
                except:
                    if self.rank == 0:
                        print(f"error restore scheds {k}, but continue.")
                    pass

        if len(error_keys) == 0 and not self.config.get("reset_epoch", False):
            self.step = state_dict["step"] + 1 
            self.epoch = state_dict["epoch"] 

        if self.rank == 0:
            log.info( f"Restore model from {cpg}, {cpd}" ) 

        # # reset learning rate
        if self.config.get("reset_learning_rate", False):
            for k in self.optims:
                for param_group in self.optims[k].param_groups:
                    param_group["lr"] = self.config["optimizer"]["learning_rate"]  
            


    def save_checkpoint(self, suffix=None): 
        suffix = str(self.step) if suffix is None else suffix 
        os.makedirs(f"{self.logdir}/ckpt", exist_ok=True) 
        save_yaml( f"{self.logdir}/ckpt/config_{suffix}.yaml", self.config )  

        state_dict = { k: self.models_test[k].state_dict() for k in self.models_test } 
        state_dict["optim"] = { k: opt.state_dict() for k, opt in self.optims.items() } 
        state_dict["scheds"] = { k: opt.state_dict() for k, opt in self.scheds.items()}
        state_dict["step"] = self.step 
        state_dict["epoch"] = self.epoch

        g_keys = [k for k in state_dict if k in self.g_keys]
        cpg = f"{self.logdir}/ckpt/g_{suffix}" 
        torch.save({ k: state_dict[k] for k in g_keys}, cpg) 
        
        i_keys = [k for k in state_dict if k not in self.g_keys]
        cpd = f"{self.logdir}/ckpt/i_{suffix}"
        torch.save({ k: state_dict[k] for k in i_keys}, cpd)

        if not sys.platform.startswith("win"):
            set_symbol_link(f"{self.logdir}/ckpt/g_{suffix}", "g_last") 
            set_symbol_link(f"{self.logdir}/ckpt/i_{suffix}", "i_last")

        self.pre_save_time = time.time() 
        if self.rank == 0:
            log.info( f"Save g model {g_keys}" )
            log.info( f"Save i model {i_keys}" )

    def _moving_average(self):
        beta = self.config.get("moving_average_beta", 0) 
        if beta == 0:
            for k in self.models:
                self.models_test[k].load_state_dict(self._models[k].state_dict()) 
        else:
            for k in self.models:
                for param, param_test in zip(self.models[k].parameters(), 
                                             self.models_test[k].parameters()): 
                    param_test.data = torch.lerp(param.data, param_test.data, beta) 
                for param, param_test in zip(self.models[k].buffers(), 
                                             self.models_test[k].buffers()): 
                    param_test.data = torch.lerp(param.data, param_test.data, beta)

    def get_learning_rate(self):
        k = list(self.optims.keys())[0]
        return self.optims[k].param_groups[0]["lr"] 


    def check_log(self, loss_dict: dict):

        if self.step % self.config["eval_step"] == 0:
            self._moving_average()  

        if self.rank != 0:
            return 
        
        config = self.config 
        if self.step % config["log_step"] == 0:
            msg  = f"Step {self.step}/{self.total_step}, Epoch {self.epoch}, " 
            msg += ", ".join([ f"{k}: {v:6f}" for k, v in loss_dict.items() ]) 
            msg += ", lr: {:.2e}".format( self.get_learning_rate() ) 

            if hasattr(self, "start_step"): 
                time_cost = (time.time() - self.start_time)/3600 
                time_total = time_cost / (self.step - self.start_step) * (
                                        self.total_step - self.start_step) 
                msg += f", Time: {time_cost:.1f}/{time_total:.1f} hour." 
            else:
                self.start_step = self.step 
                self.start_time = time.time() 

            log.info(msg) 
            log.sw_loss("train", loss_dict, self.step,name=self.name) 

        # if self.step % config["save_step"] == 0:
        #     self.save_checkpoint() 
        
        if not hasattr(self, "pre_save_time"):
            self.pre_save_time = time.time()
        elif time.time() - self.pre_save_time > 3600: 
            # save model on each hour 
            self.save_checkpoint(suffix="temp")

        # if self.step % self.config['eval_step'] == 0:
        #     self.evaluate() 
        #     torch.cuda.empty_cache()
            
        if self.step % self.config["synthesis_step"] == 0:
            self.synthesis() 
            torch.cuda.empty_cache()



        if  self.config.get("reset_d",False) and self.step % self.config["rewarm_step"] == 0:
            [self.reset_model_parameters(self.models[k]) for k in self.i_keys]
            
        


    def _init_extra(self):
        self.extra = {}

    @torch.no_grad()
    def synthesis(self):
        """Run the trainer-specific synthesis hook with inference models.

        The base implementation deliberately owns only orchestration.  Concrete
        trainers decide how to select inputs, generate samples, and persist
        results in ``_synthesis``.
        """
        if self.rank != 0:
            return None

        self._moving_average()
        models = self.models_test
        training_modes = {name: model.training for name, model in models.items()}
        for model in models.values():
            model.eval()

        try:
            return self._synthesis(models)
        finally:
            for name, model in models.items():
                model.train(training_modes[name])

    def _synthesis(self, models):
        """Trainer-specific synthesis extension point."""
        return None



    def _forward(self, batch, models, isTrain, step, epoch):

        loss_dict = dict()
        loss_dict['total_loss'] = 0

        return loss_dict


    def _update_g(self,loss_dict):
        ################ g pass #########
       
        

        g_loss = loss_dict['total_loss']

        update_g_keys = [k for k in self.g_keys if k in self.optims]
        [ self.optims[k].zero_grad() for k in update_g_keys ]
        g_loss.backward() 
        [ torch.nn.utils.clip_grad_norm_(self.models[k].parameters(), 
            self.config["optimizer"]["grad_clip_thresh"]) for k in update_g_keys ]
        [ self.optims[k].step() for k in update_g_keys ] 



    def _forward_independent(self,batch, models, isTrain, step, epoch):
        '''
        陈瑄培 2025-06-29
        因为需要训练 discriminator
        增加了 forward_d 为了让 discriminator 和 generator 单独训练
        '''
        return {}


    def _update_independent(self,loss_dict):
        '''
        陈瑄培 2025-06-29
        因为需要训练 _update_d
        用来更新 d 的参数
        '''
        if 'inde_loss' not in loss_dict:
            return
        inde_loss = loss_dict['inde_loss']
        #print(d_loss)
        
        update_inde_keys = [k for k in self.i_keys if k in self.optims]
        
        [ self.optims[k].zero_grad() for k in update_inde_keys ]
        inde_loss.backward() 
        [ torch.nn.utils.clip_grad_norm_(self.models[k].parameters(), 
            self.config["optimizer"]["grad_clip_thresh"]) for k in update_inde_keys ]
        [ self.optims[k].step() for k in update_inde_keys ] 

    def predict(self,batch,models,isTrain,step,epoch):
        return batch


    @torch.no_grad()
    def choose_action(self,batch,extra_keys=[],isTrain=False):#如果是一个动作记得加[batch]
        models = self.models
        #print(1)
        [ models[k].train() if isTrain else models[k].eval() for k in models ] 
        if "mask" in batch[0]:
            mask=batch[0]["mask"]
        else:
            mask=None
        #print(2)
        batch=[self.dataset.get_sample_preprocess(b,extra_keys) for b in batch]
        #print(3)
        batch=self.dataset.collate_state(batch,extra_keys)
        #print(4)
        batch=batch_to_cuda(batch, self.rank)
        #print(5)
        batch=self.predict(batch,models,False,self.step,self.epoch)
        #print(6)
        actions=batch['actions']
        
        if mask is not None:
            #print(7)
            actions[mask==False]=0
            #print(8)
            dist=torch.distributions.Categorical(actions)
            act=dist.sample().item()
            batch["action"]=act
        #print(9)

        return batch


    def embedding_store(self,state,data):
        pass

    def store_embedding_to_tensorboard(self):
        if self.embedding_store_data is not None:
            # print(self.embedding_store_data.keys())
            for k in self.embedding_store_data:
                self.embedding_store_data[k] = _collate_batch(
                    self.embedding_store_data[k],
                    [],
                    ["embedding","label"],
                )
            for key in self.embedding_store_data:
                # print(self.embedding_store_data[key]["embedding"].shape)
                # print(self.embedding_store_data[key]["label"].shape)
                log.sw_add_embedding(
                    "embedding/"+key, 
                    self.embedding_store_data[key]["embedding"],
                    self.embedding_store_data[key]["label"] , 
                    global_step=self.step
                )
            self.embedding_store_data = None


    def reset_model_parameters(self,model):
        for layer in model.modules():
            if hasattr(layer, 'reset_parameters'):
                layer.reset_parameters()



class EmptyTrainer(BaseTrainer):
    def __init__(self, config,restore_step, rank=0, n_gpus=1,name="main"):
        self.config = config
        self.n_gpus = n_gpus 
        self.rank = rank 
        self.name=name

        self.logdir = f'{ORGPATH}/../{CHECKPOINT_ROOT_PATH}/{config["log_dir"]}'
        #print(self.logdir)
        self.total_step = config["total_step"] 
        self.step = 0 
        self.epoch = 0 
        self._init_dataset()

    def restore_checkpoint(self, restore_step):
        self.step = 0 if restore_step == -1 else int(restore_step)

    

class ModelTrainer:

    # - "is_g" flag: [default true], optimizer assigned; 
    #         if false, it will not be updated automatically;
    #         if false, saved to d_model; 
    #         Usually for Discriminator, that need seperate update and not used for generation.
    # - "ignore_optim" flag: [default false], no optimizer assigned, thus not updated; 
    #         Usually for fixed/frozen models;

    def __init__(self, config, restore_step, rank=0, n_gpus=1):

        #------------------basic------------------
        self.config = config 
        self.n_gpus = n_gpus 
        self.rank = rank 

        random.seed(config["seed"]) 
        np.random.seed(config["seed"]) 
        torch.manual_seed(config["seed"])
        torch.cuda.manual_seed(config["seed"]) 
        torch.cuda.set_device(rank) 

        if self.rank == 0:
            log.info( "Config:\n" + yaml.safe_dump(config) ) 

        #-----------------models------------------
        self.models_config = config["model"] 
        self.models_class = { k: get_class_by_name(cfg["class_name"]) 
                              for k, cfg in config["model"].items() } 
        self.models = dict() 
        self._models = dict() 
        self.models_test = dict()
        self.optims = dict()
        self.g_keys = []
        self.d_keys = []
        for k, cfg in config["model"].items():
            model = init_model(cfg).cuda(rank)  
            if whether_contain_parameters(model):
                if self.n_gpus > 1:
                    #  DistributedDataParallel
                    #  the batch won't be split, but update in parallel for each gpu, thus faster update frequence
                    model = nn.SyncBatchNorm.convert_sync_batchnorm(model) 
                    model = DDP(model, device_ids=[rank]) 
                    if self.rank == 0: 
                        log.info(f"Using DistributedDataParallel with {self.n_gpus} gpus.")
                if self.n_gpus < -1:
                    #  DataParallel
                    #  the batch will be split in net.forward(), thus larger batch, but same update frequence
                    #  Arbitrary positional and keyword inputs are allowed to be passed into
                    #  DataParallel but some types are specially handled. tensors will be
                    #  **scattered** on dim specified (default 0). tuple, list and dict types will
                    #  be shallow copied. The other types will be shared among different threads
                    #  and can be corrupted if written to in the model's forward pass.
                    model = nn.DataParallel(model)
                    if self.rank == 0: 
                        log.info(f"Using DataParallel with {abs(self.n_gpus)} gpus.")

                if not cfg.get("ignore_optim", False):
                    #to save gpu resources
                    self.optims[k] = AdamW( model.parameters(), 
                                        lr=config["optimizer"]["learning_rate"], 
                                        betas=config["optimizer"]["betas"],
                                        eps=config["optimizer"]["eps"],
                                        weight_decay=config['optimizer'].get('weight_decay', 1e-2)) 

            if cfg.get("is_g", True):
                self.g_keys.append(k)
            else:
                self.d_keys.append(k)

            self.models[k] = model
            if self.n_gpus > 1:
                self._models[k] = model.module
            elif self.n_gpus < -1:
                self._models[k] = model.module
            else:
                self._models[k] = model

            self.models_test[k] = init_model(cfg).cuda(rank) 
            self.models_test[k].load_state_dict(self._models[k].state_dict())  

        # A training group owns a set of models, one optimizer pass and one
        # forward function.  A model may only belong to one group, otherwise a
        # later group could accidentally propagate gradients into an earlier
        # one.  Keeping this logic in the trainer (instead of the dataset)
        # makes the data/model boundary explicit.
        self.train_groups = self._build_train_groups()
        
        self.logdir = f'{CHECKPOINT_ROOT_PATH}/{config["log_dir"]}'
        if rank == 0: 
            log.init(self.logdir)
            if config.get("tensorboard_auto_start", False):
                log.start_tensorboard(
                    self.logdir,
                    host=config.get("tensorboard_host", "127.0.0.1"),
                    port=config.get("tensorboard_port", 6006),
                )
            for k in self.g_keys:
                log.info( "Network of {}: \n{}".format(k, self.models[k]) ) 
            for k in self.d_keys:
                log.info( "Discriminator of {}: \n{}".format(k, self.models[k]) ) 
            #log.info( "Config:\n" + yaml.safe_dump(config) ) 

        self.total_step = config["total_step"] 
        self.step = 0 
        self.epoch = 0 

        if self.config["optimizer"]["n_warmup_steps"] < 0:
            self.scheds = { k: ExponentialLR( opt, gamma=self.config["scheduler"]["gamma"]) 
                        for k, opt in self.optims.items() } 
        else:
            warmup_steps = self.config["optimizer"]["n_warmup_steps"] // self.config["scheduler"]["step_size"]
            total_steps  = self.config["total_step"] // self.config["scheduler"]["step_size"]

            def lr_lambda(current_step):
                if current_step < warmup_steps:
                    return float(current_step) / float(max(1, warmup_steps))
                # after warm-up: linearly decay back to 0
                return max(
                    0.0,
                    float(total_steps - current_step) / float(max(1, total_steps - warmup_steps))
                )
            self.scheds = { k: LambdaLR(opt, lr_lambda) for k, opt in self.optims.items() }

        if restore_step != 0:
            self.restore_checkpoint(restore_step) 

        self._init_dataloader()
        self._init_extra()


    def _build_train_groups(self):
        """Validate and normalize the optional ``train_groups`` config.

        Example::

            train_groups:
              body:
                models: [body_encoder, body_decoder]
                forward: _forward_body
              face:
                models: [face_encoder, face_decoder]
                forward: _forward_face

        Without ``train_groups`` the original single ``_forward`` behavior is
        used, so existing projects remain compatible.
        """
        groups_config = self.config.get("train_groups")
        if not groups_config:
            return {
                "default": {
                    "models": list(self.models),
                    "forward": "_forward",
                    "optimizers": list(self.optims),
                }
            }

        groups = {}
        owners = {}
        for group_name, group_config in groups_config.items():
            model_names = list(group_config.get("models", []))
            if not model_names:
                raise ValueError(f"train_groups.{group_name}.models cannot be empty")

            unknown = [name for name in model_names if name not in self.models]
            if unknown:
                raise ValueError(
                    f"train group '{group_name}' contains unknown models: {unknown}"
                )

            for model_name in model_names:
                if model_name in owners:
                    raise ValueError(
                        f"model '{model_name}' belongs to both '{owners[model_name]}' "
                        f"and '{group_name}'. A model can only belong to one train group."
                    )
                owners[model_name] = group_name

            forward_name = group_config.get("forward", f"_forward_{group_name}")
            if not callable(getattr(self, forward_name, None)):
                raise ValueError(
                    f"train group '{group_name}' requires trainer method '{forward_name}'"
                )

            groups[group_name] = {
                "models": model_names,
                "forward": forward_name,
                "optimizers": [name for name in model_names if name in self.optims],
            }

        trainable_models = set(self.optims)
        missing = sorted(trainable_models - set(owners))
        if missing:
            raise ValueError(
                "Every trainable model must belong to a train group. Missing: "
                f"{missing}. Add them to train_groups or set ignore_optim: true."
            )
        return groups


    def _run_group_forward(self, group_name, batch, models, isTrain):
        """Run one group with access only to the models owned by that group."""
        group = self.train_groups[group_name]
        group_models = {name: models[name] for name in group["models"]}
        forward = getattr(self, group["forward"])
        losses = forward(
            batch, group_models, isTrain=isTrain, step=self.step, epoch=self.epoch
        )
        if not isinstance(losses, dict) or "total_loss" not in losses:
            raise ValueError(
                f"{group['forward']} must return a dict containing 'total_loss'"
            )
        return losses


    @staticmethod
    def _merge_group_losses(group_losses):
        """Prefix per-group metrics so logs stay unambiguous."""
        merged = {}
        totals = []
        single_group = len(group_losses) == 1
        for group_name, losses in group_losses.items():
            for key, value in losses.items():
                if key == "total_loss":
                    totals.append(value)
                if single_group and ModelTrainer._tensorboard_only_metric(key):
                    merged[key] = value
                else:
                    merged[f"{group_name}/{key}"] = value
        if totals:
            merged["total_loss"] = sum(totals)
        return merged

    @staticmethod
    def _tensorboard_only_metric(key):
        metric_names = {"score", "pck", "error"}
        return any(part in metric_names for part in key.split("/"))

    @staticmethod
    def _metric_to_float(value):
        if torch.is_tensor(value):
            return float(value.detach().float().cpu())
        return float(value)

    @staticmethod
    def _pck_curve_metric(key):
        parts = key.split("/")
        return any(
            parts[index] == "pck" and parts[index + 1] == "curve"
            for index in range(len(parts) - 1)
        )

    @staticmethod
    def _tensorboard_metric_tag(split, key):
        parts = key.split("/")
        metric_names = {"score", "pck", "error"}
        metric_index = next(
            (index for index, part in enumerate(parts) if part in metric_names),
            None,
        )
        if metric_index is None:
            return f"{split}/{key}"

        metric = parts[metric_index]
        group = "_".join(parts[:metric_index])
        split_prefix = f"{split}_{group}" if group else split
        remaining = parts[metric_index + 1 :]

        if metric == "score":
            if remaining[:1] == ["joint"]:
                suffix = remaining[1:]
                base = f"{split_prefix}_joint_score"
            else:
                suffix = remaining
                base = f"{split_prefix}_score"
        elif metric == "error":
            if remaining[:1] == ["joint"]:
                suffix = remaining[1:]
                if suffix[-1:] == ["mean"]:
                    suffix = suffix[:-1]
                base = f"{split_prefix}_joint_error"
            else:
                suffix = remaining
                base = f"{split_prefix}_error"
        elif metric == "pck":
            if remaining[:1] == ["curve"]:
                suffix = remaining[1:]
                base = f"{split_prefix}_pck_curve"
            else:
                suffix = remaining
                base = f"{split_prefix}_pck"

        return f"{base}/{'/'.join(suffix)}" if suffix else base

    def _write_tensorboard_metrics(self, tag, loss_dict):
        for key, value in loss_dict.items():
            if self._pck_curve_metric(key):
                continue
            log.sw_scalar(
                self._tensorboard_metric_tag(tag, key),
                value,
                self.step,
            )
        self._write_tensorboard_curves(tag, loss_dict)

    def _write_tensorboard_curves(self, tag, loss_dict):
        curves = {}
        for key, value in loss_dict.items():
            parts = key.split("/")
            for index in range(len(parts) - 2):
                if parts[index] == "pck" and parts[index + 1] == "curve":
                    try:
                        threshold = float(parts[index + 2])
                    except ValueError:
                        continue
                    curve_key = "/".join(parts[: index + 2])
                    curves.setdefault(curve_key, []).append(
                        (threshold, self._metric_to_float(value))
                    )
                    break

        for curve_key, points in curves.items():
            points = sorted(points, key=lambda item: item[0])
            thresholds = [point[0] for point in points]
            values = [point[1] for point in points]
            log.sw_curve(
                self._tensorboard_metric_tag(tag, f"{curve_key}/curve"),
                thresholds,
                values,
                self.step,
                xlabel="Normalized error threshold",
                ylabel="PCK",
            )

    def _reset_eval_metrics(self):
        pass

    def _finalize_eval_metrics(self, loss_dict):
        return loss_dict


    def _init_dataloader(self):
        config = self.config 
        self.dataset_class = get_class_by_name(config["dataset_class_name"])
        dataset = self.dataset_class(config, mode="train") 
        self.dataset = dataset 

        if self.n_gpus > 1:
            sampler = DistributedSampler(dataset, self.n_gpus, self.rank, drop_last=True, shuffle=True) 
            self.dataloader = DataLoader(dataset, 
                                batch_size=config["dataloader"]["batch_size"], 
                                collate_fn=dataset.collate_fn, 
                                num_workers=config["dataloader"]["num_workers"], 
                                sampler=sampler,
                                prefetch_factor=config["dataloader"].get("prefetch_factor", 2),
                                persistent_workers=config["dataloader"].get("persistent_workers", False),
                                pin_memory=config["dataloader"].get("pin_memory", False)) 
        else:
            n_devices = abs(self.n_gpus)
            batch_size = config["dataloader"]["batch_size"] * n_devices
            if n_devices > 1:
                log.info(f"Update batch size to {batch_size} with {n_devices} gpus.")
            self.dataloader = DataLoader(dataset, 
                                batch_size=batch_size, 
                                collate_fn=dataset.collate_fn, 
                                num_workers=config["dataloader"]["num_workers"],
                                drop_last=True,
                                shuffle=True,
                                prefetch_factor=config["dataloader"].get("prefetch_factor", 2),
                                persistent_workers=config["dataloader"].get("persistent_workers", False),
                                pin_memory=config["dataloader"].get("pin_memory", False)) 


    def restore_checkpoint(self, restore_step):

        if restore_step == -1:
            cpg = read_symbol_link(f"{self.logdir}/ckpt/g_last")
            cpd = read_symbol_link(f"{self.logdir}/ckpt/d_last")
        else:
            cpg = f"{self.logdir}/ckpt/g_{restore_step}" 
            cpd = f"{self.logdir}/ckpt/d_{restore_step}"
        if not os.path.isfile(cpg): 
            raise ValueError(f"Not find checkpoint for {restore_step} step") 
        
        state_dict = {} 
        state_dict.update( torch.load(cpg, weights_only=True, map_location="cpu") )
        if os.path.isfile(cpd):
            state_dict.update( torch.load(cpd, weights_only=False, map_location="cpu") ) 

        error_keys = []
        for k in self._models:
            try:
                self._models[k].load_state_dict(state_dict[k], strict=False)
                self.models_test[k].load_state_dict(state_dict[k], strict=False) 
            except:
                if self.rank == 0:
                    log.info(f"error restore model {k}, but continue.")
                error_keys.append(k)
        
        #there might be error if d model is not found, fix later
        if len(error_keys) == 0:
            for k in self.optims:
                try:
                    self.optims[k].load_state_dict( state_dict["optim"][k]) 
                except:
                    if self.rank == 0:
                        print(f"error restore optims {k}, but continue.")
                    error_keys.append(k)
                    pass
            for k in self.scheds:
                try:
                    self.scheds[k].load_state_dict( state_dict["scheds"][k]) 
                except:
                    if self.rank == 0:
                        print(f"error restore scheds {k}, but continue.")
                    pass

        if len(error_keys) == 0 and not self.config.get("reset_epoch", False):
            self.step = state_dict["step"] + 1 
            self.epoch = state_dict["epoch"] 

        if self.rank == 0:
            log.info( f"Restore model from {cpg}, {cpd}" ) 


    def save_checkpoint(self, suffix=None): 
        suffix = str(self.step) if suffix is None else suffix 
        os.makedirs(f"{self.logdir}/ckpt", exist_ok=True) 
        save_yaml( f"{self.logdir}/ckpt/config_{suffix}.yaml", self.config )  

        state_dict = { k: self.models_test[k].state_dict() for k in self.models_test } 
        state_dict["optim"] = { k: opt.state_dict() for k, opt in self.optims.items() } 
        state_dict["scheds"] = { k: opt.state_dict() for k, opt in self.scheds.items()}
        state_dict["step"] = self.step 
        state_dict["epoch"] = self.epoch

        g_keys = [k for k in state_dict if k in self.g_keys]
        cpg = f"{self.logdir}/ckpt/g_{suffix}" 
        torch.save({ k: state_dict[k] for k in g_keys}, cpg) 
        
        d_keys = [k for k in state_dict if k not in self.g_keys]
        cpd = f"{self.logdir}/ckpt/d_{suffix}"
        torch.save({ k: state_dict[k] for k in d_keys}, cpd)

        if not sys.platform.startswith("win"):
            set_symbol_link(f"{self.logdir}/ckpt/g_{suffix}", "g_last") 
            set_symbol_link(f"{self.logdir}/ckpt/d_{suffix}", "d_last")

        self.pre_save_time = time.time() 
        if self.rank == 0:
            log.info( f"Save g model {g_keys}" )
            log.info( f"Save d model {d_keys}" )

    def _moving_average(self):
        beta = self.config.get("moving_average_beta", 0) 
        if beta == 0:
            for k in self.models:
                self.models_test[k].load_state_dict(self._models[k].state_dict()) 
        else:
            for k in self.models:
                for param, param_test in zip(self.models[k].parameters(), 
                                             self.models_test[k].parameters()): 
                    param_test.data = torch.lerp(param.data, param_test.data, beta) 
                for param, param_test in zip(self.models[k].buffers(), 
                                             self.models_test[k].buffers()): 
                    param_test.data = torch.lerp(param.data, param_test.data, beta)

    def get_learning_rate(self):
        k = list(self.optims.keys())[0]
        return self.optims[k].param_groups[0]["lr"] 


    def check_log(self, loss_dict: dict):

        if self.step % self.config["eval_step"] == 0:
            self._moving_average()  

        if self.rank != 0:
            return 
        
        config = self.config 
        if self.step % config["log_step"] == 0:
            msg  = f"Step {self.step}/{self.total_step}, Epoch {self.epoch}, " 
            log_items = {
                k: v
                for k, v in loss_dict.items()
                if not self._tensorboard_only_metric(k)
            }
            msg += ", ".join([ f"{k}: {v:6f}" for k, v in log_items.items() ])
            msg += ", lr: {:.2e}".format( self.get_learning_rate() ) 

            if hasattr(self, "start_step"): 
                time_cost = (time.time() - self.start_time)/3600 
                time_total = time_cost / (self.step - self.start_step) * (
                                        self.total_step - self.start_step) 
                msg += f", Time: {time_cost:.1f}/{time_total:.1f} hour." 
            else:
                self.start_step = self.step 
                self.start_time = time.time() 

            log.info(msg) 
            self._write_tensorboard_metrics("train", loss_dict)

        if self.step % config["save_step"] == 0:
            self.save_checkpoint() 
        
        if not hasattr(self, "pre_save_time"):
            self.pre_save_time = time.time()
        elif time.time() - self.pre_save_time > 3600: 
            # save model on each hour 
            self.save_checkpoint(suffix="temp")

        if self.step % self.config['eval_step'] == 0:
            self.evaluate() 
            torch.cuda.empty_cache()
            
        if self.step % self.config["synthesis_step"] == 0:
            self.synthesis() 
            torch.cuda.empty_cache()
        

    def check_eval_log(self, loss_dict: dict):
        if self.rank != 0 :
            return 
        self._write_tensorboard_metrics("eval", loss_dict)


    def run(self):

        models = self.models
        [ models[k].train() for k in models ] 

        print( f"Rank {self.rank}, start training" ) 

        # reset learning rate
        if self.config.get("reset_learning_rate", False):
            for k in self.optims:
                for param_group in self.optims[k].param_groups:
                    param_group["lr"] = self.config["optimizer"]["learning_rate"]  

        while True:
            for batch in self.dataloader:

                batch = batch_to_cuda(batch, self.rank)
                group_losses = {}
                for group_name, group in self.train_groups.items():
                    update_keys = group["optimizers"]
                    for key in update_keys:
                        self.optims[key].zero_grad()

                    losses = self._run_group_forward(
                        group_name, batch, models, isTrain=True
                    )
                    group_loss = losses["total_loss"]
                    if update_keys:
                        group_loss.backward()
                        for key in update_keys:
                            torch.nn.utils.clip_grad_norm_(
                                self.models[key].parameters(),
                                self.config["optimizer"]["grad_clip_thresh"],
                            )
                            self.optims[key].step()
                    group_losses[group_name] = losses

                loss_dict = self._merge_group_losses(group_losses)

                self.check_log(loss_dict) 
                
                if self.step >= self.total_step:
                    if self.rank == 0:
                        self.save_checkpoint() 
                        log.info("Finish training.") 
                    return 
                
                if self.step % self.config["scheduler"]["step_size"] == 0:
                    [ self.scheds[k].step() for k in self.scheds ] 

                self.step += 1 
            self.epoch += 1


    @torch.no_grad()
    def evaluate(self):

        models = self.models_test
        [ models[k].eval() for k in models ] 

        dataset = self.dataset_class(self.config, "test") 
        loader = DataLoader( 
            dataset, 
            batch_size=self.config["dataloader"]["batch_size"],  #too large will make loss count inbalance #self.config["dataloader"]["batch_size"], 
            shuffle=True,
            drop_last=False,
            collate_fn=dataset.collate_fn,
            num_workers=1
        )

        loss_dict_sum = None

        count = 0
        total = min(len(dataset), self.config.get("test_items", 30))
        self._reset_eval_metrics()
        for batch in tqdm.tqdm(loader,'Evaluation'):

            batch = batch_to_cuda(batch, self.rank)
            group_losses = {
                name: self._run_group_forward(name, batch, models, isTrain=False)
                for name in self.train_groups
            }
            loss_dict = self._merge_group_losses(group_losses)
            if loss_dict_sum is None:
                loss_dict_sum = loss_dict
            else:
                for k in loss_dict:
                    loss_dict_sum[k] += loss_dict[k]
            count += 1
            if count > total:
                break

        for k in loss_dict_sum:
            loss_dict_sum[k] = loss_dict_sum[k] / count
        loss_dict_sum = self._finalize_eval_metrics(loss_dict_sum)
        self.check_eval_log(loss_dict_sum)


    @torch.no_grad() 
    def synthesis(self):

        save_dir = os.path.join(self.logdir, "synthesis") 
        os.makedirs(save_dir, exist_ok=True)
        os.makedirs(f"{save_dir}/{self.step}", exist_ok=True)

        models = self.models_test
        [ models[k].eval() for k in models ] 
        
        dataset = self.dataset_class(self.config, "synthesis")
        synthesis_num_workers = int(
            self.config.get("synthesis_num_workers", 0)
        )
        if synthesis_num_workers < 0:
            raise ValueError("synthesis_num_workers must be non-negative")
        loader_kwargs = {
            "dataset": dataset,
            "batch_size": 1,
            "shuffle": not self.config.get("synthesis_fixed_items", True),
            "drop_last": False,
            "collate_fn": dataset.collate_fn,
            "num_workers": synthesis_num_workers,
            "pin_memory": bool(
                self.config.get(
                    "synthesis_pin_memory",
                    self.config.get("dataloader", {}).get("pin_memory", False),
                )
            ),
        }
        if synthesis_num_workers > 0:
            loader_kwargs["prefetch_factor"] = int(
                self.config.get("synthesis_prefetch_factor", 2)
            )
        loader = DataLoader(**loader_kwargs)

        total, idx = min(len(dataset), self.config.get("synthesis_items", 10)), 0
        for batch in tqdm.tqdm(loader, "Synthesis", total=total):
            if idx >= total:
                break

            batch = batch_to_cuda(batch, self.rank)
            index = batch["index"][0] 
            save_name = f"{save_dir}/{self.step}/{index}"

            self._synthesis(batch, models, save_name, idx)

            ################ loop #############
            idx += 1

    def _init_extra(self):
        self.extra = {}


    def _forward(self, batch, models, isTrain, step, epoch):

        loss_dict = dict()
        loss_dict['total_loss'] = 0

        return loss_dict
    

    @torch.no_grad() 
    def _synthesis(self, batch, models, save_name, idx):
        pass


    # def _finetune(self, model, input, gt, save_model):
        
    #     optimizer = AdamW(model.parameters(), 
    #                 lr=1e-4, 
    #                 betas=[0.8, 0.99],
    #                 eps=1.0e-9,
    #                 weight_decay=1e-2)

    #     loss = nn.L1Loss()(input, gt.detach()) 

    #     optimizer.zero_grad()
    #     g_loss.backward() 
    #     optimizer.step()

    #     state_dict = { k: self.mbert_models[k].state_dict() for k in self.mbert_models } 
    #     torch.save({ k: state_dict[k] for k in state_dict}, save_file) 
