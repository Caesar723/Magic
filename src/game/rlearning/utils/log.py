
import os 
from loguru import logger 
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt

from torch.utils.tensorboard import SummaryWriter 


SW = None 
INIT_STATE = False

def init(logdir, use_tensorboard=True):
    global INIT_STATE, SW
    if not INIT_STATE:
        os.makedirs(logdir, exist_ok=True) 
        logger.add( os.path.join(logdir, "{time:YYYYMMDD-HHmmss}.log") ) 
        INIT_STATE = True

    if use_tensorboard and SW is None:
        SW = SummaryWriter(logdir) 

def sw_loss(tag, loss_dict, global_step,name=""):
    for k in loss_dict:
        SW.add_scalar( f"{name}/{tag}/{k}", loss_dict[k], global_step) 

def sw_audio(tag, audio, sample_rate, global_step=None):
    global SW 
    SW.add_audio(tag, audio, sample_rate=sample_rate, 
                        global_step=global_step) 

def sw_figure_lines(tag, datas, labels, global_step):
    fig = plt.figure()
    for data, lab in zip(datas, labels):
        plt.plot(data, label=lab) 
    plt.legend()
    SW.add_figure(tag, fig, global_step=global_step) 

def sw_figure(tag, data, global_step):
    if type(data) is matplotlib.figure.Figure:
        fig = data 
    else:
        fig = plt.figure()
        plt.imshow(data)
    SW.add_figure(tag, fig, global_step=global_step) 

def sw_video(tag, video, global_step):
    SW.add_video(tag, video, global_step=global_step, fps=30)

debug = logger.debug
info = logger.info 
warn = logger.warning
error = logger.error 

