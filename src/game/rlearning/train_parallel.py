import sys
if __name__=="__main__":
    from pathlib import Path
    src_root = next(parent for parent in Path(__file__).resolve().parents if parent.name == "src")
    if str(src_root) not in sys.path:
        sys.path.append(str(src_root))
import argparse
import torch.multiprocessing as mp
from initinal_file import ORGPATH
from game.rlearning.utils.model import get_class_by_name
from game.rlearning.utils.file import read_yaml



def main(args):
    config_path=args.config
    config=read_yaml(config_path)
    env=get_class_by_name(config["env"])(config_path, restore_step=args.restore_step)
    try:
        env.start_worker()
        env.run()
    except KeyboardInterrupt:
        print("\nInterrupted by user; saving checkpoint and stopping child processes...")
        # Parallel_Env owns ``agent1`` directly.  Pair exercise is a
        # launcher for child Parallel_Env instances, so it deliberately has
        # no top-level trainer to checkpoint here.
        agent = getattr(env, "agent1", None)
        if agent is not None and agent.rank == 0:
            agent.save_checkpoint()
    finally:
        env.shutdown()


def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-c","--config",type=str,default=f"{ORGPATH}/game/rlearning/config/parallel/specific/parallel_specific_v1.yaml")
    parser.add_argument(
        "-r", "--restore-step", type=int, default=None,
        help="Checkpoint step to restore; use -1 for the latest g_last/i_last checkpoint.",
    )
    return parser.parse_args()


if __name__=="__main__":
    mp.set_start_method("spawn")
    args=get_args()
    main(args)
