class Animation{//action

    constructor(object_hold,player){///object can be card and 
        this.object_hold=object_hold
        this.player=player

    }

    set_animate(){//

    }

    ability(){//改变血量之类的

    }


}


class Creature_Start_Attack extends Animation{
    constructor(object_hold,player,attack_obj,state_self,state_attacted){///object can be card and 
        super(object_hold,player)
    }
}
class Creature_Prepare_Attack extends Animation{
    constructor(object_hold,player){///object can be card and 
        super(object_hold,player)
    }
}
class Creature_Prepare_Defense extends Animation{
    constructor(object_hold,player){///object can be card and 
        super(object_hold,player)
    }
}
class Activate_Ability extends Animation{
    constructor(object_hold,player){///object can be card and 
        super(object_hold,player)
    }
}

class Select_Object extends Animation{
    constructor(object_hold,player,selected_object){///object can be card and 
        super(object_hold,player)
        this.selected_object=selected_object
        

    }

    set_animate(){

    }

    ability(){

    }
}
class Add_Buff extends Select_Object{

}

class Attack_To_Object extends Select_Object{

}


class Cure_To_Object extends Select_Object{

}
class Gain_Card extends Select_Object{

}
class Lose_Card extends Select_Object{

}

class Die extends Animation{
    constructor(object_hold,player){///object can be card and 
        super(object_hold,player)
    }
}
class Summon extends Animation{
    constructor(object_hold,player){///object can be card and 
        super(object_hold,player)
    }
}

class Turn extends Animation{
    constructor(object_hold,player){///object can be card and 
        super(object_hold,player)
    }
}
class Change_Mana extends Animation{
    constructor(object_hold,player){///object can be card and 
        super(object_hold,player)
    }
}
