if __name__=="__main__":
    import sys
    sys.path.append("/Users/xuanpeichen/Desktop/code/python/openai/src")
    
   

#from room_server import RoomServer
import numpy as np
import asyncio
#from game.train_agent import Agent_Train_Red as Agent_Train
from game.room import Room
from game.ppo_train import Agent_PPO
from game.player import Player
from game.agent import Agent_Player as Agent
import torch
import random
from torch import nn
from game.type_cards.creature import Creature
from game.type_cards.instant import Instant
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery
from game.player_agent_room import PVE_Room
from game.game_recorder import GameRecorder
from game.game_function_tool import ORGPATH

class Expert_Demonstrate_Room(PVE_Room):
    pass




