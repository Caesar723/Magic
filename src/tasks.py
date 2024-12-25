

class Task:

    name:str
    description:str
    total_steps:int
    gold_reward:int

    def get_progress(counter_dict:dict,flag_dict:dict)->int:
        pass

class KillTask(Task):
    name="KillTask"
    description="Kill 50 creatures"
    total_steps=50
    gold_reward=100

    def get_progress(counter_dict:dict,flag_dict:dict)->int:
        return counter_dict.get("kill_creature_count",0)

class DrawTask(Task):
    name="DrawTask"
    description="Draw 50 cards"
    total_steps=50
    gold_reward=200
    def get_progress(counter_dict:dict,flag_dict:dict)->int:
        return counter_dict.get("draw_card_count",0)

class PlayCardTask(Task):
    name="PlayCardTask"
    description="Play 30 cards"
    total_steps=30
    gold_reward=100
    def get_progress(counter_dict:dict,flag_dict:dict)->int:
        return counter_dict.get("play_card_count",0)
    
class WinTask(Task):
    name="WinTask"
    description="Win 1 game"
    total_steps=1
    gold_reward=100
    def get_progress(counter_dict:dict,flag_dict:dict)->int:
        return flag_dict.get("win",0)

class Win5Task(Task):
    name="WinTask"
    description="Win 5 games"
    total_steps=5
    gold_reward=600
    def get_progress(counter_dict:dict,flag_dict:dict)->int:
        return flag_dict.get("win",0)

class UseSorceryTask(Task):
    name="UseSorceryTask"
    description="Use 10 sorceries"
    total_steps=10
    gold_reward=100
    def get_progress(counter_dict:dict,flag_dict:dict)->int:
        return counter_dict.get("use_sorcery_count",0)

class SpendLandTask(Task):
    name="SpendLandTask"
    description="Spend 50 lands"
    total_steps=50
    gold_reward=100
    def get_progress(counter_dict:dict,flag_dict:dict)->int:
        return counter_dict.get("spend_land_count",0)
    
TASK_DICT={}#used to store task name and task class
for cla in Task.__subclasses__():
    TASK_DICT[cla.__name__]=cla