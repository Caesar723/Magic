if __name__=="__main__":
    import sys
    from pathlib import Path
    src_root = next(parent for parent in Path(__file__).resolve().parents if parent.name == "src")
    if str(src_root) not in sys.path:
        sys.path.append(str(src_root))
    
   

#from room_server import RoomServer
import numpy as np
import asyncio
#from game.train_agent import Agent_Train_Red as Agent_Train
from game.room import Room
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




