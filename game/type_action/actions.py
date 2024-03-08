
from game.action import Action



class Creature_Start_Attack(Action):
    pass

class Creature_Prepare_Attack(Action):
    pass

class Creature_Prepare_Defense(Action):
    pass


class Activate_Ability(Action):
    pass

class Select_Object(Action):
    pass

class Add_Buff(Select_Object):
    pass


class Attack_To_Object(Select_Object):#这种伤害自己的随从是不会受伤的
    pass

class Cure_To_Object(Select_Object):
    pass

class Gain_Card(Select_Object):
    pass

class Die(Action):
    pass


class Summon(Action):
    pass