from typing import TYPE_CHECKING
from functools import wraps
from game.rlearning.utils.simulation_scenarios import ScenarioTools
import random
if TYPE_CHECKING:
    from rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.card import Card
    from game.player import Player



def simulate(func=None, *, evidence=None):
    labels = evidence or {}
    text_parts = tuple(labels.get("text", ()))
    field_names = tuple(labels.get("fields", ()))

    def decorate(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            outer=not getattr(self,"_scenario_running",False)
            if outer:
                self.room.clear_environmrnt()
                self.scenario_begin(method)
                self._scenario_running=True
            try:
                result=method(self,*args,**kwargs)
                if outer:
                    result=self.scenario_finish(result)
                result["description_info"]=self.build_description()
                result["supervision"]={"text_parts":list(text_parts),"fields":list(field_names)}
                return result
            finally:
                if outer:
                    self._scenario_running=False

        wrapper._is_simulate = True
        return wrapper

    return decorate(func) if func is not None else decorate

def bind_card(card_cls):
    def decorator(simulation_cls):
        simulation_cls.card_cls = card_cls
        return simulation_cls
    return decorator

def test(simulation_cls):
    simulation_cls._is_test = True
    return simulation_cls

class Card_Simulation(ScenarioTools):
    
    card:"Card"
    _is_test:bool=False
    similar_descriptions:list[str]=[]
    text_parts = {}

    ADJECTIVES = [
    "Aether", "Void", "Rune", "Sky", "Ember",
    "Mystic", "Storm", "Moonlit", "Iron", "Arcane",
    "Ancient", "Crimson", "Golden", "Shadow",
    "Celestial", "Wild", "Silent", "Burning",
    "Frost", "Sacred", "Twilight", "Forgotten"
    ]

    NOUNS = [
        "Sage", "Scholar", "Adept", "Archivist",
        "Seeker", "Channeler", "Weaver", "Oracle",
        "Scribe", "Wanderer", "Invoker", "Guardian",
        "Prophet", "Mage", "Knight", "Spirit",
        "Shaman", "Watcher", "Herald", "Warden",
        "",
        "",
        "",
    ]

    SUFFIXES = [
        "",
        "",
        "",
        "of the Vale",
        "of Twilight",
        "of Embers",
        "of Storms",
        "of the Deep",
        "of Ashes",
        "of Eternity",
    ]

    def __init__(self,player:"Player",room:"Multi_Agent_Parallel_Specific_Room"):
        self.player=player
        self.room=room
        if self.card_cls is None:
            raise ValueError(f"{type(self).__name__} do not bind card_cls")

        self.card = self.card_cls(player)

    def random_card_name(self):
        adj = random.choice(self.ADJECTIVES)
        noun = random.choice(self.NOUNS)
        suffix = random.choice(self.SUFFIXES)
        if noun=="":
            return f"{adj}"

        if suffix:
            return f"{adj} {noun} {suffix}"
        return f"{adj} {noun}"


    def get_similar_description(self):
        if not self.similar_descriptions:
            return self.card.content
        description = random.choice(self.similar_descriptions)

        description = description.replace(
            "[CARD_NAME]",
            self.random_card_name()
        )

        return description

    def build_description(self):
        if not self.text_parts:
            return {"text": self.card.content, "spans": {}}

        values = self.description_values()
        text, spans = "", {}

        for part_id, phrases in self.text_parts.items():
            fragment = random.choice(phrases).format(**values)
            text += " " if text else ""

            start = len(text)
            text += fragment
            spans[part_id] = [(start, len(text))]

        extra = " ".join(self.card.extra_content)
        if extra:
            text += " " + extra

        return {"text": text, "spans": spans}


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
    def basic_initinal(self,parameters:dict={
        "graveyard":{"creature_number":(0,10),"instant_number":(0,10),"sorcery_number":(0,10),"land_number":(0,10)},
        "hand":{"creature_number":(0,2),"instant_number":(0,2),"sorcery_number":(0,2),"land_number":(0,2)},
        "library":{"creature_number":(0,10),"instant_number":(0,10),"sorcery_number":(0,10),"land_number":(0,10)},
    }):
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
