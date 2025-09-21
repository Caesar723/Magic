import os
import importlib

import torch   
import torch.nn as nn
import torch.nn.functional as F

from game.rlearning.utils.file import read_symbol_link


def get_class_by_name(class_name):
    path = class_name.split(".") 
    if len(path) == 1:
        raise ValueError(f"Please provide package path: [{class_name}]") 
    
    package = importlib.import_module( ".".join(path[:-1]) ) 
    class_handler = getattr(package, path[-1]) 
    return class_handler 
    

def init_model(config):
    model_class = get_class_by_name(config["class_name"]) 
    try:
        mcfg = { k: v for k, v in config.items() if k not in ("class_name", "is_g", "ignore_optim") } 
        model = model_class(**mcfg) 
    except:
        model = model_class(config)
    return model  


def zero_module(module):
    """
    Zero out the parameters of a module and return it.
    """
    for p in module.parameters():
        p.detach().zero_()
    return module

def set_symbol_link(link_file, symbol, overwrite=True):
    link_dir, fn = os.path.split(link_file)
    link_path = os.path.join(link_dir, symbol)
    if os.path.islink(link_path) and overwrite:
        os.remove(link_path)
    os.symlink(fn, link_path)
    
def load_model(checkpoint, config, rank, strict=False, debug=False):
 
    if checkpoint is not None and os.path.islink(checkpoint):
        checkpoint = read_symbol_link(checkpoint)
    
    models_config = config["model"]
    models = {} 
    for k, cfg in models_config.items():
        if models_config[k].get("is_g", True):
            models[k] = init_model(cfg).cuda(rank)

    if checkpoint is None:
        return models

    state_dict = torch.load(checkpoint, weights_only=True, map_location=lambda storage, loc: storage) #map_location="cpu") #
    if "state_dict" in state_dict:
        state_dict = state_dict["state_dict"]

    if debug:
        for m in state_dict:
            print(f"checkpoint {checkpoint}: {m}")

    for k in models:
        if k not in state_dict:
            print(f"model {k} fail to load state dict.")
            continue
        if rank == 0:
            print(f"load model state dict of {k}")
        #models[k] = nn.DataParallel(models[k])
        models[k].load_state_dict(state_dict[k], strict=strict) 
        if hasattr(models[k], "remove_weight_norm"):
            models[k].remove_weight_norm()
        models[k].eval() 

    if rank == 0:
        print(f"load model from {checkpoint}")

    return models



def load_ckpt(model, ckpt_path):
    if not os.path.exists(ckpt_path):
        print(f"Checkpoint {ckpt_path} doesn't exist")
        return
    state_dict = torch.load(ckpt_path, map_location='cuda:0')
    if 'state_dict' in state_dict.keys():
        state_dict = state_dict['state_dict']

    from collections import OrderedDict
    new_state_dict = OrderedDict()
    model_state_dict = model.state_dict()
    for k, v in state_dict.items():
        if k.startswith('module.'):
            name = k[7:]
        else:
            name = k
        if name in model_state_dict and v.shape == model_state_dict[name].shape:
            new_state_dict[name] = v
        elif name == 'conv1.weight' and v.shape[1] == 3 and model_state_dict[name].shape[1] == 1:
            new_state_dict[name] = torch.mean(v, 1, keepdim=True)
        else:
            print("Warning: {} (shape: {}) in the checkpoint cannot be loaded into the network".format(k, v.shape))
    model.load_state_dict(new_state_dict, strict=False)
    print(f"{ckpt_path} loaded")



def update_model(base_checkpoint, updated_checkpoint, model_names):

    state_dict_base = torch.load(base_checkpoint, map_location="cpu")
    print("base_checkpoint: ", state_dict_base.keys())
    state_dict_update = torch.load(updated_checkpoint, map_location="cpu")
    print("updated_checkpoint: ", state_dict_update.keys())

    for m in model_names:
        if m in state_dict_update:
            print(f"adding/replacing model {m}")
            state_dict_base[model_names[m]] = state_dict_update[m]

    if "optim" in state_dict_base:
        print("optim: ", state_dict_base["optim"].keys())
        print("optim2: ", state_dict_update["optim"].keys())

        for m in model_names:
            if m in state_dict_update["optim"]:
                print(f"adding/replacing optim {m}")
                state_dict_base["optim"][model_names[m]] = state_dict_update["optim"][m]

    torch.save(state_dict_base, f"{base_checkpoint}_merged") 

    print(f"saved merged model to {base_checkpoint}_merged")



def rename_model(checkpoint, renames):

    state_dict_base = torch.load(checkpoint, map_location="cpu")
    for m in renames:
        if m in state_dict_base:
            print(f"adding/replacing model {m}")
            state_dict_base[renames[m]] = state_dict_base[m]
            state_dict_base.pop(m)

    torch.save(state_dict_base, f"{checkpoint}_renamed") 

    print(f"saved renamed model to {checkpoint}_renamed")




def merge_model(checkpoint1, checkpoint2, rename_list1, rename_list2, save_file):

    if type(checkpoint1) is str:
        state_dict1 = torch.load(checkpoint1, map_location="cpu")
    else:
        state_dict1 = checkpoint1
    print("checkpoint1: ", state_dict1.keys())
    if type(checkpoint2) is str:
        state_dict2 = torch.load(checkpoint2, map_location="cpu")
    else:
        state_dict2 = checkpoint2
    print("checkpoint2: ", state_dict2.keys())

    state_dict_merged = {}
    for m in rename_list1:
        m_new = rename_list1[m]
        state_dict_merged[m_new] = state_dict1[m]
    for m in rename_list2:
        m_new = rename_list2[m]
        state_dict_merged[m_new] = state_dict2[m]

    for m in state_dict_merged:
        print(f"merged: model {m}")

    if save_file is not None:
        torch.save(state_dict_merged, f"{save_file}") 
        print(f"saved merged model to {save_file} {state_dict_merged.keys()}")

    return state_dict_merged

    

def whether_contain_parameters(model: torch.nn.Module):
    p = model.parameters()
    try:
        next(p) 
        return True 
    except StopIteration:
        return False


def sequence_mask(length, max_length=None):
    if max_length is None:
        max_length = length.max()
    x = torch.arange(max_length, dtype=length.dtype, device=length.device)
    return x.unsqueeze(0) < length.unsqueeze(1)


def padding_mask(length, max_length=None):
    if max_length is None:
        max_length = length.max()
    x = torch.arange(max_length, dtype=length.dtype, device=length.device)
    return x.unsqueeze(0) >= length.unsqueeze(1)

def get_model(config,cache={}):
    key=config["log_dir"]+"_"+str(config["restore_step"])

    if key in cache:
        return cache[key]
    else:
        model_class=get_class_by_name(config["trainer"])
        agent=model_class(config,config["restore_step"],name="agent1")
        cache[key]=agent
        return agent

def main():
    pass


if __name__ == '__main__':
    main()