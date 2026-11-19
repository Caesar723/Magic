
import os
import sys
from loguru import logger 



SW = None 
INIT_STATE = False

def init(logdir, use_tensorboard=True):
    global INIT_STATE, SW
    if not INIT_STATE:
        os.makedirs(logdir, exist_ok=True) 
        logger.add( os.path.join(logdir, "{time:YYYYMMDD-HHmmss}.log") ) 
        INIT_STATE = True

    if use_tensorboard and SW is None:
        if os.environ.get("WANDB_MODE", "disabled") in ("online", "offline") and os.environ.get("RL_ROLLOUT_WORKER") != "1":
            try:
                import wandb
                wandb.init(
                    project=os.environ.get("WANDB_PROJECT", "magic"),
                    name=os.environ.get("WANDB_NAME") or os.path.basename(os.path.normpath(logdir)),
                    dir=logdir,
                    sync_tensorboard=True,
                    save_code=False,
                    settings=wandb.Settings(init_timeout=15, console="off", _disable_stats=True),
                )
                wandb.define_metric("global_step")
                wandb.define_metric("*", step_metric="global_step")
            except Exception as error:
                logger.warning("W&B unavailable; TensorBoard logging continues: {}", error)

        from torch.utils.tensorboard import SummaryWriter
        SW = SummaryWriter(logdir)

def sw_loss(tag, loss_dict, global_step,name=""):
    for k in loss_dict:
        SW.add_scalar( f"{name}/{tag}/{k}", loss_dict[k], global_step) 

def sw_scalar(tag, value, global_step):
    if SW is None:
        return
    if hasattr(value, "detach"):
        value = value.detach()
    SW.add_scalar(tag, value, global_step)

def sw_curve(tag, x, y, global_step, xlabel=None, ylabel=None):
    if SW is None:
        return
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    fig, axis = plt.subplots()
    axis.plot(x, y)
    if xlabel:
        axis.set_xlabel(xlabel)
    if ylabel:
        axis.set_ylabel(ylabel)
    SW.add_figure(tag, fig, global_step=global_step)
    plt.close(fig)

def sw_audio(tag, audio, sample_rate, global_step=None):
    global SW 
    SW.add_audio(tag, audio, sample_rate=sample_rate, 
                        global_step=global_step) 

def sw_figure_lines(tag, datas, labels, global_step):
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    fig = plt.figure()
    for data, lab in zip(datas, labels):
        plt.plot(data, label=lab) 
    plt.legend()
    SW.add_figure(tag, fig, global_step=global_step) 


def sw_add_embedding(tag, data, label, global_step):
    SW.add_embedding(data, tag=tag, metadata=label, global_step=global_step)

def sw_figure(tag, data, global_step):
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    if type(data) is matplotlib.figure.Figure:
        fig = data 
    else:
        fig = plt.figure()
        plt.imshow(data)
    SW.add_figure(tag, fig, global_step=global_step) 

def sw_video(tag, video, global_step):
    SW.add_video(tag, video, global_step=global_step, fps=30)

def close():
    if SW is not None:
        SW.close()
    if "wandb" in sys.modules:
        try:
            sys.modules["wandb"].finish(exit_code=int(sys.exc_info()[0] is not None))
        except Exception as error:
            logger.warning("W&B finish failed: {}", error)


debug = logger.debug
info = logger.info 
warn = logger.warning
error = logger.error 
