import os
import json

from game.game_function_tool import get_cards_diction,get_cards_simulation_diction


CARD_DICTION=get_cards_diction()
CARD_SIMULATION_DICTION=get_cards_simulation_diction()
ORGPATH=os.path.dirname(os.path.abspath(__file__))

