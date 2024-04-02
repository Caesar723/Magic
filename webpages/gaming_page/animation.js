class Animation{//action

    constructor(object_hold,player){///object can be card and 
        this.object_hold=object_hold
        this.player=player

        this.width=50
        this.height=50

        this.canvas=document.createElement('canvas');
        this.canvas.width = this.width
        this.canvas.height = this.height
        this.ctx=this.canvas.getContext('2d')
        this.set_canvas()
        this.arrow_img=new Image();

    }

    set_animate(){//

    }
    ability(){//改变血量之类的

    }
    set_canvas(){
        
        this.ctx.clearRect(0,0,this.canvas.width,this.canvas.height)
        this.ctx.save()
        this.ctx.beginPath();
        this.draw_rect_smooth(this.ctx,0,0,this.width,this.height)
        this.ctx.closePath();
        this.ctx.clip();
        this.ctx.drawImage(this.object_hold.orginal_image,0,0,this.width,this.height)


        this.ctx.beginPath();
        this.draw_rect_smooth(this.ctx,0,0,this.width,this.height)
        this.ctx.strokeStyle = 'rgb(22,34,41)';
        this.ctx.shadowColor = 'rgb(22,34,41)'; // 半透明的蓝色光晕
        // 设置阴影的模糊级别
        this.ctx.shadowBlur = 10;
        // 设置阴影的偏移量
        this.ctx.shadowOffsetX = 0;
        this.ctx.shadowOffsetY = 0;
        this.ctx.lineWidth = 5;
        this.ctx.stroke(); // 描绘边框
        this.ctx.closePath();
        this.ctx.restore()
    }

    

    draw_image(ctx,index){
        this.set_canvas()

        const y=20+index*(this.height+20)
        const x=80

        ctx.drawImage(this.canvas,x,y,this.width,this.height)

        ctx.beginPath();
        this.draw_rect_smooth(this.ctx,x,y,this.width,this.height)
        ctx.strokeStyle = 'rgb(22,34,41)';
        ctx.shadowColor = 'rgb(22,34,41)'; // 半透明的蓝色光晕
        // 设置阴影的模糊级别
        ctx.shadowBlur = 10;
        // 设置阴影的偏移量
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;
        ctx.lineWidth = 10;
        ctx.stroke(); // 描绘边框
        ctx.closePath();
    }

    draw_rect_smooth(ctx,x,y,width,height){
        
        
        var radius = 10; // 圆角半径

        // 绘制圆角长方形路径
        
        ctx.moveTo(x + radius, y);
        ctx.lineTo(x + width - radius, y);
        ctx.arcTo(x + width, y, x + width, y + radius, radius);
        ctx.lineTo(x + width, y + height - radius);
        ctx.arcTo(x + width, y + height, x + width - radius, y + height, radius);
        ctx.lineTo(x + radius, y + height);
        ctx.arcTo(x, y + height, x, y + height - radius, radius);
        ctx.lineTo(x, y + radius);
        ctx.arcTo(x, y, x + radius, y, radius);
        
    }
    check_mouse(mouse_pos,index){
        
        const y=20+index*(this.height+20)
        const x=80-70
        //console.log(mouse_pos,x,y)
        if (x<mouse_pos[0] && mouse_pos[0]<x+this.width && y<mouse_pos[1] && mouse_pos[1]<y+this.height){
            return true
        }
        else{
            return false
        }
    }

    update_cards(){
        this.object_hold.position[0]=-20
        this.object_hold.update()
    }
    draw_action(ctx,canvas,camera){
        this.object_hold.draw(camera,ctx,canvas)
        ctx.drawImage(this.arrow_img,canvas.width/2-100,canvas.height/2-100,300,200)
    }


}


class Creature_Start_Attack extends Animation{
    constructor(object_hold,player,attack_obj,state_self,state_attacted){///object can be card and 
        super(object_hold,player)
        this.attacked_obj=attack_obj
        this.state_self=state_self
        this.state_attacted=state_attacted

    }
}
class Creature_Prepare_Attack extends Animation{
    constructor(object_hold,player){///object can be card and 
        super(object_hold,player)
    }
}
class Creature_Prepare_Defense extends Animation{
    constructor(object_hold,player,attack_obj){///object can be card and 
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
