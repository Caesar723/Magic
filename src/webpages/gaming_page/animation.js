class Animation{//action

    constructor(object_hold,player){///object can be card and 
        this.name="Action"
        this.object_hold=object_hold
        console.log(object_hold)
        if (this.object_hold instanceof Player){
            this.new_ring_hold=this.object_hold.player_life_ring.get_copy()
        }
        else{
            this.object_hold=Animation.check_hand(this.object_hold)
            this.object_hold_new=this.object_hold.get_copy()
        }
        
        console.log(object_hold)
        this.player=player

        this.width=50
        this.height=50

        this.canvas=document.createElement('canvas');
        this.canvas.width = this.width
        this.canvas.height = this.height
        this.ctx=this.canvas.getContext('2d')
        this.set_canvas()
        this.arrow_img=new Image();

        this.action_finished=false

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

        if (this.object_hold instanceof Player){
            this.new_ring_hold.update(this.player.camera)
            this.ctx.drawImage(this.new_ring_hold.canvas,0,0,this.width,this.height)
            //this.new_ring.draw(camera,ctx,canvas)
        }
        else{
            //console.log(this.object_hold)
            this.ctx.drawImage(this.object_hold.orginal_image,0,0,this.width,this.height)
        }
        //console.log(this.ctx,this.object_hold.orginal_image,this.object_hold)
        


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

        
        this.draw_rect_smooth(this.ctx,x,y,this.width,this.height)
        ctx.beginPath();
        
        if (this.player instanceof Opponent){
            ctx.strokeStyle = 'rgb(22,34,41)';
            ctx.shadowColor = 'rgb(22,34,41)'; // 半透明的蓝色光晕
            //console.log(this,x,y)
        }
        else{
            ctx.strokeStyle = 'rgb(242,246,252)';
            ctx.shadowColor = 'rgb(242,246,252)'; // 半透明的蓝色光晕
        }

        
        // 设置阴影的模糊级别
        ctx.shadowBlur = 10;
        // 设置阴影的偏移量
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;
        ctx.lineWidth = 10;
        
        ctx.stroke(); // 描绘边框
        
        ctx.closePath();

        ctx.drawImage(this.canvas,x,y,this.width,this.height)
        

        
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
        if (this.object_hold instanceof Player){
            //this.new_ring=this.object_hold.player_life_ring.get_copy()
            
            this.new_ring_hold.position[0]=-20
            
            this.new_ring_hold.update(this.player.camera)
        }
        else{
            this.object_hold.position[0]=-20
            
            this.object_hold.update()
        }
        
    }
    draw_action(ctx,canvas,camera){
        if (this.object_hold instanceof Player){
            // this.new_ring.update(camera)
            // this.ctx.drawImage(this.new_ring.canvas,0,0,this.width,this.height)
            this.new_ring_hold.position[0]=-20
            this.new_ring_hold.update(camera)
            this.new_ring_hold.draw(camera,ctx,canvas)
        }
        else{
            this.object_hold_new.position[0]=-20
            this.object_hold_new.update()
            this.object_hold_new.draw(camera,ctx,canvas)
        }

        ctx.font = "80px serif";
        ctx.textBaseline = "middle";
        ctx.textAlign = "center";
        ctx.fillStyle = "#e3b931";
        ctx.shadowColor = "#e3b931";
        ctx.shadowBlur = 20;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;
        const mid_x = ctx.canvas.width / 2;
        const mid_y = ctx.canvas.height / 5;
        ctx.fillText(this.name, mid_x, mid_y);
        ctx.shadowColor = "transparent";
        ctx.shadowBlur = 0;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;
        
        //ctx.drawImage(this.arrow_img,canvas.width/2-100,canvas.height/2-100,300,200)
    }

    finished(){
        return true
    }
    static check_battle(card){//如果card是hand，检查有没有battle，没有就建一个
        if (card instanceof Card_Battle || card instanceof Card_Hand_Oppo){
            return card
        }
        else if(card instanceof Creature_Hand || card instanceof Land_Hand){
            if (card.battle===undefined && card instanceof Land_Hand){
                
                new Land_Battle(6,5,[-25,-20,0],0.3,card,card.player.type_name,card.player.table)
            }
            else if (card.battle===undefined && card instanceof Creature_Hand){
                if (card.player instanceof Self){
                    for (let card_batt of  card.player.table.self_battlefield){
                        if (card_batt.id==card.id){
                            card.battle=card_batt
                            return card.battle
                        }
                    }
                }
                else{
                    for (let card_batt of  card.player.table.opponent_battlefield){
                        if (card_batt.id==card.id){
                            card.battle=card_batt
                            return card.battle
                        }
                    }
                }
                new Creature_Battle(6,5,[-25,-20,0],0.3,card,card.player.type_name,card.player.table)
            }
            return card.battle
        }
    }
    static check_hand(card,battle_bool){//如果card是battle，变成hand，如果battle_bool是true，检查有没有battle，没有就建一个
        if (battle_bool){
            this.check_battle(card)
        }
        if (card instanceof Card_Battle){
            return card.card
        }
        else if(card instanceof Card_Hand || card instanceof Card_Hand_Oppo){
            return card
        }
    }


}


class Creature_Start_Attack extends Animation{
    constructor(object_hold,player,attack_obj,state_self,state_attacted){///object can be card and 
        super(object_hold,player)
        //this.attacked_obj=Animation.check_battle(attack_obj)
        this.state_self=state_self
        this.state_attacted=state_attacted
        this.name='Creature Start Attack'

        //console.log(attack_obj)

        
        if (attack_obj instanceof Player){
            this.attacked_obj=attack_obj
            this.new_ring=attack_obj.player_life_ring.get_copy()
            this.new_ring.life=state_attacted[0]
        }
        else{
            this.attacked_obj=Animation.check_battle(attack_obj)
            this.new_card=this.attacked_obj.card.get_copy()
            this.new_card.Life=state_attacted[1]
            this.new_card.Damage=state_attacted[0]
        }


    }
    set_animate(){//

        this.object_hold=Animation.check_hand(this.object_hold,true)
        if (this.attacked_obj instanceof Player){
            this.object_hold.battle.moving_cache.push(["rotate_to_point",[this.attacked_obj.player_life_ring.position]])
            this.object_hold.battle.moving_cache.push(["attack_to",[this.attacked_obj.player_life_ring.position,this.state_self,this.attacked_obj,this.state_attacted]])
        }
        else if (this.attacked_obj instanceof Creature_Battle){
            this.object_hold.battle.moving_cache.push(["rotate_to_point",[this.attacked_obj.position]])
            this.object_hold.battle.moving_cache.push(["attack_to",[this.attacked_obj.position,this.state_self,this.attacked_obj,this.state_attacted]])
        }
        this.object_hold.battle.moving_cache.push(["rotate_to_point",[[
            this.object_hold.battle.accurate_position[0],
            this.object_hold.battle.accurate_position[1],
            this.object_hold.battle.accurate_position[2]+1,
        ]]])

        // if (this.player instanceof Opponent){
        //     this.object_hold.battle.moving_cache.push(["rotate_to_point",[[
        //         this.object_hold.battle.accurate_position[0],
        //         this.object_hold.battle.accurate_position[1],
        //         this.object_hold.battle.accurate_position[2]-1,
        //     ]]])
        // }
        // else{
        //     this.object_hold.battle.moving_cache.push(["rotate_to_point",[[
        //         this.object_hold.battle.accurate_position[0],
        //         this.object_hold.battle.accurate_position[1],
        //         this.object_hold.battle.accurate_position[2]+1,
        //     ]]])
        // }
        
    }
    draw_action(ctx,canvas,camera){
        super.draw_action(ctx,canvas,camera)
        
        ctx.drawImage(this.arrow_img,canvas.width/2-100,canvas.height/2-100,300,200)

        if (this.attacked_obj instanceof Player){
            
            this.new_ring.position[0]=20
            this.new_ring.update(camera)
            this.new_ring.draw(camera,ctx,canvas)
        }
        else{
            this.new_card.position[0]=20
            this.new_card.update()
            this.new_card.draw(camera,ctx,canvas)
        }
    }

    finished(){
        //console.log(this.object_hold.battle.moving)
        return !this.object_hold.battle.moving
    }
}
class Creature_Prepare_Attack extends Animation{
    constructor(object_hold,player){///object can be card and 
        super(object_hold,player)
        this.name='Creature Prepare Attack'
    }
    set_animate(){
        this.object_hold.battle.mode="attack"
        this.object_hold.battle.moving_cache.push(["rotate_to_point",[this.player.oppo.player_life_ring.position]])
    }
    draw_action(ctx,canvas,camera){
        super.draw_action(ctx,canvas,camera)
        
        
    }
}
class Play_Cards extends Animation{
    constructor(object_hold,player,show_2D){///object can be card and 
        super(object_hold,player)
        this.show_2D=show_2D
        
        this.action_finished=false
        this.name='Play Card'
    }
    set_animate(){
        //this.deleted_card.moving_cache.push(["disappear",[[0,60*this.player.unit,-20]]])
        this.show_2D.show_a_card(this.object_hold)
        setTimeout(() => {
            this.action_finished=true
            this.show_2D.unshow_a_card()
          }, 2000); // 将在2秒后打印消息
    }
    draw_action(ctx,canvas,camera){
        super.draw_action(ctx,canvas,camera)
        
        
    }
    finished(){
        return this.action_finished
    }
}
class Creature_Prepare_Defense extends Animation{
    constructor(object_hold,player,attack_obj){///object can be card and 
        super(object_hold,player)
        this.attacked_obj=attack_obj
        this.new_card=Animation.check_hand(this.attacked_obj).get_copy()
        this.name='Creature Prepare Defense'
    }
    set_animate(){
        this.object_hold=Animation.check_hand(this.object_hold,true)
        this.object_hold.battle.mode="defence"
        this.object_hold.battle.moving_cache.push(["rotate_to_point",[this.attacked_obj.position]])
    }


    draw_action(ctx,canvas,camera){
        
        super.draw_action(ctx,canvas,camera)
        ctx.drawImage(this.arrow_img,canvas.width/2-100,canvas.height/2-100,300,200)

        
        this.new_card.position[0]=20
        this.new_card.update()
        this.new_card.draw(camera,ctx,canvas)
        
    }
    finished(){
        return !this.object_hold.battle.moving
    }

}
class Activate_Ability extends Animation{//就是将卡牌横置
    constructor(object_hold,player){///object can be card and 
        super(object_hold,player)
        this.name='Activate Ability'

    }
    set_animate(){
        this.object_hold=Animation.check_hand(this.object_hold,true)
        
        //console.log(this.object_hold.battle,this.object_hold)
        this.object_hold.battle.z_index=-1;
        this.object_hold.battle.activated=true
        this.object_hold.battle.moving_cache.push(["rotate_to_point",[0]])
        
        // console.log(this.object_hold.battle.accurate_position,this.object_hold.battle.position,[
        //     this.object_hold.battle.accurate_position[0]+1,
        //     this.object_hold.battle.accurate_position[1],
        //     this.object_hold.battle.accurate_position[2],
        // ])
    //    this.object_hold.battle.moving_cache.push(["rotate_to_point",[[
    //     this.object_hold.battle.accurate_position[0]+1,
    //     this.object_hold.battle.accurate_position[1],
    //     this.object_hold.battle.accurate_position[2],
    // ]]])
    }
    draw_action(ctx,canvas,camera){
        super.draw_action(ctx,canvas,camera)
        
    }
    // finished(){
    //     return !this.object_hold.battle.moving
    // }

}
class Reset_Ability extends Animation{//就是将卡牌解除横置
    constructor(object_hold,player){///object can be card and 
        super(object_hold,player)
        this.name='Reset Ability'

    }
    set_animate(){
        this.object_hold=Animation.check_hand(this.object_hold,true)
        this.object_hold.battle.z_index=1;
        this.object_hold.battle.activated=false
        this.object_hold.battle.moving_cache.push(["rotate_to_point",[[
            this.object_hold.battle.accurate_position[0],
            this.object_hold.battle.accurate_position[1],
            this.object_hold.battle.accurate_position[2]+1,
        ]]])
        
    //    this.object_hold.battle.moving_cache.push(["rotate_to_point",[[
    //     this.object_hold.battle.accurate_position[0]+1,
    //     this.object_hold.battle.accurate_position[1],
    //     this.object_hold.battle.accurate_position[2],
    // ]]])
    }
    draw_action(ctx,canvas,camera){
        super.draw_action(ctx,canvas,camera)
        
    }
}

class Select_Object extends Animation{
    constructor(object_hold,player,selected_object){///object can be card and 
        super(object_hold,player)
        if (selected_object instanceof Player){
            this.selected_object=selected_object
        }
        else{
            this.selected_object=Animation.check_hand(selected_object)
        }
        this.name='Select Object'
        

    }

    set_animate(){

    }

    ability(){

    }
}
class Add_Buff extends Select_Object{
    constructor(object_hold,player,selected_object,color,type,final_state,buff){//selected_object hand or battle
        super(object_hold,player,selected_object)
        //console.log(selected_object.buff_list)
        this.final_state=final_state
        this.buff=buff
        this.special_effect=player.table.special_effects
        

        
        this.action_finished=true
        this.name='Add Buff'
        this.color=color
        this.type=type
        
        this.new_card=Animation.check_hand(this.selected_object).get_copy()
        this.new_card.Life=final_state[1]
        this.new_card.Damage=final_state[0]
        

        this.missile=undefined
        
    }
    set_animate(){
        this.selected_object.append_buff(this.buff)
        //console.log(this.selected_object)
        if (this.selected_object.type=="Creature"){
            if (this.type=="None"){
                this.selected_object.change_state(...this.final_state)
            }
            else{
                if (this.object_hold.type=="Creature"){
                    this.object_hold=Animation.check_hand(this.object_hold,true)
                    this.missile=this.special_effect.create_missile(this.object_hold,this.selected_object,this.color,this.type,this.final_state)
                }
                else
                {
                    this.missile=this.special_effect.create_missile(this.object_hold.player,this.selected_object,this.color,this.type,this.final_state)
                }
                
                this.player.music.play_music_effect("missile")
            
            }
        }

    }
    draw_action(ctx,canvas,camera){
        super.draw_action(ctx,canvas,camera)
        ctx.drawImage(this.arrow_img,canvas.width/2-100,canvas.height/2-100,300,200)

        this.new_card.position[0]=20
        this.new_card.update()
        this.new_card.draw(camera,ctx,canvas)
    }
    finished(){
        if (this.type=="None"){
            if (this.missile===undefined){
                return true;
            }
            else{
                return this.missile.disappear
            }
        }
        else{
            return true
        }
        //return this.action_finished
    }
}
class Lose_Buff extends Select_Object{
    constructor(object_hold,player,selected_object,final_state,buff){//selected_object hand or battle
        super(object_hold,player,selected_object)
        this.final_state=final_state
        this.buff=buff
        

        this.new_card=Animation.check_hand(this.selected_object).get_copy()

        this.action_finished=true
        this.name='Add Buff'
        //console.log(object_hold,player,selected_object,final_state,buff)
        
    }
    set_animate(){
        //console.log("change")
        this.selected_object.remove_buff(this.buff)
        if (this.selected_object.type=="Creature"){
            //console.log(this.selected_object,this.final_state)
            this.selected_object.change_state(...this.final_state)
        }
        

    }
    draw_action(ctx,canvas,camera){
        super.draw_action(ctx,canvas,camera)
        ctx.drawImage(this.arrow_img,canvas.width/2-100,canvas.height/2-100,300,200)

        this.new_card.position[0]=20
        this.new_card.update()
        this.new_card.draw(camera,ctx,canvas)
    }
    finished(){
        
        return this.action_finished
    }
}
class Attack_To_Object extends Select_Object{
    constructor(object_hold,player,selected_object,color,type,result_state){//selected_object hand
        super(object_hold,player,selected_object)
        this.special_effect=player.table.special_effects
        this.color=color
        this.type=type
        this.result_state=result_state
        this.name='Attack To Object'


        if (this.selected_object instanceof Player){
            this.new_ring=this.selected_object.player_life_ring.get_copy()
            this.new_ring.life=result_state[0]
        }
        else{
            this.new_card=Animation.check_hand(this.selected_object).get_copy()
            this.new_card.Life=result_state[1]
            this.new_card.Damage=result_state[0]
        }


        this.missile=undefined

    }
    set_animate(){
        
        console.log(this.object_hold)
        
        this.missile=this.special_effect.create_missile(this.object_hold,this.selected_object,this.color,this.type,this.result_state)
        this.player.music.play_music_effect("missile")

    }
    draw_action(ctx,canvas,camera){
        super.draw_action(ctx,canvas,camera)
        ctx.drawImage(this.arrow_img,canvas.width/2-100,canvas.height/2-100,300,200)


        if (this.selected_object instanceof Player){
            
            this.new_ring.position[0]=20
            this.new_ring.update(camera)
            this.new_ring.draw(camera,ctx,canvas)
        }
        else{
            this.new_card.position[0]=20
            this.new_card.update()
            this.new_card.draw(camera,ctx,canvas)
        }
    }
    finished(){
        if (this.missile===undefined){
            return true;
        }
        else{
            return this.missile.disappear
        }
    }
}


class Cure_To_Object extends Select_Object{
    constructor(object_hold,player,selected_object,color,type,result_state){//selected_object hand
        super(object_hold,player,selected_object)
        this.special_effect=player.table.special_effects
        this.color=color
        this.type=type
        this.result_state=result_state
        this.name='Cure To Object'


        if (this.selected_object instanceof Player){
            this.new_ring=this.selected_object.player_life_ring.get_copy()
            this.new_ring.life=result_state[0]
        }
        else{
            this.new_card=Animation.check_hand(this.selected_object).get_copy()
            this.new_card.Life=result_state[1]
            this.new_card.Damage=result_state[0]
        }

        this.missile=undefined


    }
    set_animate(){
        console.log(this.object_hold)
        this.missile=this.special_effect.create_missile(this.object_hold,this.selected_object,this.color,this.type,this.result_state)
        this.player.music.play_music_effect("missile")


    }
    draw_action(ctx,canvas,camera){
        super.draw_action(ctx,canvas,camera)
        ctx.drawImage(this.arrow_img,canvas.width/2-100,canvas.height/2-100,300,200)


        if (this.selected_object instanceof Player){
            
            this.new_ring.position[0]=20
            this.new_ring.update(camera)
            this.new_ring.draw(camera,ctx,canvas)
        }
        else{
            this.new_card.position[0]=20
            this.new_card.update()
            this.new_card.draw(camera,ctx,canvas)
        }
    }
    finished(){
        if (this.missile===undefined){
            return true;
        }
        else{
            return this.missile
        }
    }

}

class Point_To extends Select_Object{
    constructor(object_hold,player,selected_object){//selected_object hand
        super(object_hold,player,selected_object)
        this.special_effect=player.table.special_effects
        if (this.selected_object instanceof Player){
            this.new_ring=this.selected_object.player_life_ring.get_copy()
            
        }
        else{
            this.new_card=Animation.check_hand(this.selected_object).get_copy()
            
        }
        
        this.name='Point To'
    }
    set_animate(){
        this.missile=this.special_effect.create_missile(this.object_hold,this.selected_object,'','Arrow','')
        //console.log(this.missile)
        //this.player.music.play_music_effect("missile")


    }
    draw_action(ctx,canvas,camera){
        super.draw_action(ctx,canvas,camera)
        ctx.drawImage(this.arrow_img,canvas.width/2-100,canvas.height/2-100,300,200)


        if (this.selected_object instanceof Player){
            
            this.new_ring.position[0]=20
            this.new_ring.update(camera)
            this.new_ring.draw(camera,ctx,canvas)
        }
        else{
            this.new_card.position[0]=20
            this.new_card.update()
            this.new_card.draw(camera,ctx,canvas)
        }
    }
    finished(){
        if (this.missile===undefined){
            return true;
        }
        else{
            return this.missile
        }
    }

}

class Gain_Card extends Select_Object{
    constructor(object_hold,player,selected_object){//selected_object hand
        super(object_hold,player,selected_object)
        this.new_card=Animation.check_hand(this.selected_object).get_copy()
        this.name='Gain Card'
    }
    set_animate(){
        this.selected_object.position=[0,60*this.player.unit,-20]
        this.player.cards.push(this.selected_object)
        this.player.music.play_music_effect("card_pic")
        //console.log(this.player.cards)
        //this.selected_object.moving_cache.push(["rotate_to_point",[this.attacked_obj.position]])
    }
    draw_action(ctx,canvas,camera){

        
        super.draw_action(ctx,canvas,camera)
        ctx.drawImage(this.arrow_img,canvas.width/2-100,canvas.height/2-100,300,200)

        this.new_card.position[0]=20
        this.new_card.update()
        this.new_card.draw(camera,ctx,canvas)
    }
}
class Lose_Card extends Select_Object{
    constructor(object_hold,player,selected_object){//selected_object hand
        super(object_hold,player,selected_object)
        this.selected_object=Animation.check_hand(selected_object,false,player)
        //console.log(this.selected_object)
        //console.log(arguments,object_hold,player,selected_object)
        this.new_card=Animation.check_hand(this.selected_object).get_copy()
        this.name='Lose Card'
        
    }
    set_animate(){
        //this.selected_object.position=[0,60*this.player.unit,-20]
        // if (this.selected_object instanceof Card_Battle){
        //     this.selected_object.moving_cache.push(["disappear",[[0,-20,-20*this.player.unit]]])
        // }
        // else{
        this.selected_object.moving_cache.push(["disappear",[[0,60*this.player.unit,-20]]])
        //}
        
        //this.player.cards.push(this.selected_object)
        //this.selected_object.moving_cache.push(["rotate_to_point",[this.attacked_obj.position]])
    }
    draw_action(ctx,canvas,camera){

        
        super.draw_action(ctx,canvas,camera)
        ctx.drawImage(this.arrow_img,canvas.width/2-100,canvas.height/2-100,300,200)

        this.new_card.position[0]=20
        this.new_card.update()
        this.new_card.draw(camera,ctx,canvas)
    }
    finished(){
        //console.log(this.selected_object.moving)
        return !this.selected_object.moving
    }
}

class Die extends Animation{
    constructor(object_hold,player){///object can be card and //object_hold battle
        super(object_hold,player)
        //this.new_card=this.object_hold.get_copy()
        this.name='Die'
    }
    set_animate(){
        this.object_hold=Animation.check_hand(this.object_hold,true)
        this.object_hold.battle.moving_cache.push(["disappear",[[0,-20,-20*this.player.unit]]])
        
    }
    draw_action(ctx,canvas,camera){

        
        super.draw_action(ctx,canvas,camera)
        //console.log(this.object_hold.size,position)
        //ctx.drawImage(this.arrow_img,canvas.width/2-100,canvas.height/2-100,300,200)

        
    }
    finished(){
        return !this.object_hold.battle.moving
    }
}

class Summon extends Animation{
    constructor(object_hold,player){///object can be card and 
        super(object_hold,player)
        this.object_hold=Animation.check_hand(object_hold,true,player)
        //console.log(object_hold)
        this.name='Summon'
    }
    set_animate(){
        //this.selected_object.position=[0,60*this.player.unit,-20]
        // console.log(this.object_hold)
        this.object_hold.battle.position=[0,-20,-20*this.player.unit]
        if (this.object_hold instanceof Creature_Hand){
            if (this.player instanceof Opponent){
                this.player.table.opponent_battlefield.push(this.object_hold.battle)
            }
            else{
                this.player.table.self_battlefield.push(this.object_hold.battle)
            }
            
        }
        else if(this.object_hold instanceof Land_Hand){
            if (this.player instanceof Opponent){
                this.player.table.opponent_landfield.push(this.object_hold.battle)
            }
            else{
                this.player.table.self_landfield.push(this.object_hold.battle)
            }
        }
        this.player.music.play_music_effect("card_send")
        

        //this.player.cards.push(this.selected_object)
        //this.selected_object.moving_cache.push(["rotate_to_point",[this.attacked_obj.position]])
        //console.log(this.object_hold)
    }
    draw_action(ctx,canvas,camera){

        
        super.draw_action(ctx,canvas,camera)
        
    }
}

class Turn extends Animation{
    constructor(object_hold,player){///object can be card and 
        super(object_hold,player)
        this.name='Turn'
    }
    set_animate(){
        // console.log(this.player,this.player.table.player_self.my_turn)
        if (this.player instanceof Opponent){
            this.player.table.timmer_turn.change_yellow()
            this.player.table.player_self.my_turn=false
        }
        else{
            this.player.table.timmer_turn.change_green()
            this.player.table.player_self.my_turn=true
        }
        // console.log(this.player.table.player_self.my_turn)
    }
}


class Change_Mana extends Animation{
    constructor(object_hold,player,mana_cost){///player must be self  mana_cost[blue,white,black,red,green]
        super(object_hold,player)
        this.mana_cost=mana_cost
        // console.log(object_hold,player,mana_cost)

        this.new_mana_bar=new Mana_Bar()
        this.new_mana_bar.set_mana(this.mana_cost)
        this.name='Change Mana'
        
    }
    set_animate(){
        // console.log(this.object_hold_new,this.player,this.mana_cost)
        this.player.mana_bar.set_mana(this.mana_cost)

    }
    draw_action(ctx,canvas,camera){
        let index=0
        for(let color in this.new_mana_bar.bars){
            this.new_mana_bar.bars[color].position[0]=1470-5*150
            this.new_mana_bar.bars[color].position[1]=index*15+canvas.height/2-100
            index++
        }
        super.draw_action(ctx,canvas,camera)
        ctx.drawImage(this.arrow_img,canvas.width/2-100,canvas.height/2-100,300,200)
        this.new_mana_bar.update()
        this.new_mana_bar.draw(canvas,ctx,camera)
        
    }
    finished(){
        //console.log(this.player.mana_bar.check_finish())
        return this.player.mana_bar.check_finish()
    }
}

class Win extends Animation{
    constructor(object_hold,player){///player must be self  mana_cost[blue,white,black,red,green]
        super(object_hold,player)

    }
    set_animate(){
        const client=this.player.table.client

        client.win_lose.set_picture(true)


        const values = [this.player.name,'close_game','win'];
        client.socket_main.send(values.join('|'));

        setTimeout(() => {
            window.location.href = '/';
        }, 5000);
    }

}

class Lose extends Animation{
    constructor(object_hold,player){///player must be self  mana_cost[blue,white,black,red,green]
        super(object_hold,player)

    }
    set_animate(){
        const client=this.player.table.client

        client.win_lose.set_picture(false)


        const values = [this.player.name,'close_game',"lose"];
        client.socket_main.send(values.join('|'));

        setTimeout(() => {
            window.location.href = '/';
        }, 5000);
        
    }

}
