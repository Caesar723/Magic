from typing import TYPE_CHECKING
from functools import wraps
import random
if TYPE_CHECKING:
    from rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.card import Card
    from game.player import Player



def simulate(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)

    wrapper._is_simulate = True
    return wrapper

def bind_card(card_cls):
    def decorator(simulation_cls):
        simulation_cls.card_cls = card_cls
        return simulation_cls
    return decorator

class Card_Simulation:
    card:"Card"

    def __init__(self,player:"Player",room:"Multi_Agent_Parallel_Specific_Room"):
        self.player=player
        self.room=room
        if self.card_cls is None:
            raise ValueError(f"{type(self).__name__} do not bind card_cls")

        self.card = self.card_cls(player)
    
    def get_card(self):
        return self.card

    def get_candidates_simulation(self):
        methods = []

        for name in dir(self):
            method = getattr(self, name)

            if not callable(method):
                continue
            func = getattr(method, "__func__", method)

            if getattr(func, "_is_simulate", False):
                methods.append(method)
        return methods

    def basic_initinal(self,parameters:dict={}):
        self.room.env_initinal_graveyard(self.player,parameters.get("graveyard",{}))
        self.room.env_initinal_hand(self.player,parameters.get("hand",{}))
        self.room.env_initinal_library(self.player,parameters.get("library",{}))

    def random_env_creature(self):
        return random.choice(
            [
                self.room.env_creature,
                self.room.env_no_creature,
                self.room.env_one_creature,
            ]
        )
    def random_life(self):
        return random.choice(
            [
                self.room.env_life_low,
                self.room.env_life_middle,
                self.room.env_life_high,
            ]
        )
        

    



    