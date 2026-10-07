from typing import TYPE_CHECKING
import numpy as np

from game.type_cards.creature import Creature
from game.type_cards.instant import Instant,Instant_Undo
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery

if TYPE_CHECKING:
    from game.agent import Agent_Player as Agent
    from game.base_agent_room import Base_Agent_Room
    






def add_history(agent:"Agent",batch):
    if "lstm_output" in batch:
        agent.lstm_output = (
            batch["lstm_output"][0]
            .detach()
            .float()
            .cpu()
            .numpy()
            .copy()
        )
