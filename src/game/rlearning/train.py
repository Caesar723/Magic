import traceback
import sys
from pathlib import Path

import torch 


src_root = Path(__file__).resolve().parents[2]
if str(src_root) not in sys.path:
    sys.path.insert(0, str(src_root))

from game.rlearning.utils.file import read_yaml
from game.rlearning.utils.model import get_class_by_name


def main(args):
    # Read Config
    config = read_yaml(args.config) 
    restore_step = args.restore_step
    
    trainer_class = get_class_by_name(config["trainer"])

    n_gpus = torch.cuda.device_count()
    trainer = trainer_class(config, restore_step, rank=0, n_gpus=-n_gpus) 
    
    try:
        trainer.run() 
    except KeyboardInterrupt as e:
        trainer.save_checkpoint()
        print( f"Exit Training" ) 
    except Exception as e:
        trainer.save_checkpoint()
        traceback.print_exc()


if __name__ == "__main__":
    import argparse, traceback
    parser = argparse.ArgumentParser()
    parser.add_argument( "-r", "--restore_step", type=int, default=0)
    parser.add_argument( "-c", "--config", type=str, required=True,
                         help="path to config.yaml", )
    args = parser.parse_args()

    main(args)
