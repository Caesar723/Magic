class Animation{//action

    constructor(object_hold,player){///object can be card and 
        this.object_hold=object_hold
        this.player=player

    }

    set_animate(){

    }

    ability(){

    }

}


class Creature_Start_Attack extends Animation{

}
class Creature_Prepare_Attack extends Animation{

}
class Creature_Prepare_Defenseextends extends Animation{

}
class Activate_Ability extends Animation{

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

}
class Summon extends Animation{

}

class Turn extends Animation{

}
class Change_Mana extends Animation{

}
