class Creature_Battle extends Card_Battle {
    constructor(width,height,position,size,card,player,table){
        super(width,height,position,size,card,player,table)
        // this.Org_Life=card.Org_Life;
        // this.Life=card.Life;
        // this.Org_Damage=card.Org_Damage;
        // this.Damage=card.Damage;
        this.Org_Life=card.Org_Life;
        this.Life=card.Life;
        this.Org_Damage=card.Org_Damage;
        this.Damage=card.Damage;
        this.type="Creature";

        this.mode="none"//none attack,defence
        this.flying=card.flying//trur-> flying
        this.current_flying=false
        this.move_to_fly_flag=false
        this.flying_x=0
        this.moving_dict["move_to_flying"]=[this.move_to_flying.bind(this),this.move_to_flying_prepared.bind(this),this.move_to_flying_finish.bind(this)]
        this.flying_height=-25
        this.unflying_height=-20
    }

    
    update(camera){
        super.update(camera);
        this.print_life_damage();

        this.check_flying()
        this.flying_motion()
        

        
    }
    print_life_damage(){
        this.create_blank_space(
            this.canvas,
            this.ctx,
            this.canvas.width*4.9/8,
            this.canvas.height*20.5/25
            )
        this.fill_text_life_power(
            this.ctx,
            this.canvas.width*4.9/8,
            this.canvas.height*23.8/25
        );
    }
    create_blank_space(canvas,ctx,startX,startY){
        const blank_color="rgb(233,233,233,0.9)"
        const squareSize_x = canvas.width*3/10; // 正方形的边长
        const squareSize_y = canvas.height*1.5/10;
        const radius = squareSize_y / 2; // 半圆的半径

        // 计算绘制的起始位置
        // const startX = canvas.width/8; // Canvas 上的起始 X 坐标
        // const startY = canvas.height*7.1/8; // Canvas 上的起始 Y 坐标

        // 绘制左侧的半圆
        ctx.beginPath();
        ctx.fillStyle = blank_color; // 改变填充颜色为蓝色
        ctx.arc(startX, startY + radius, radius, 0.5 * Math.PI, 1.5 * Math.PI);
        
        ctx.fill();
        ctx.fillStyle = 'rgb(0,0,0,1)'; // 改变填充颜色为蓝色
        ctx.stroke(); // 绘制半圆的描边

        // 绘制正方形
        ctx.fillStyle = blank_color; // 改变填充颜色为蓝色
        ctx.fillRect(startX, startY, squareSize_x, squareSize_y);
        ctx.fillStyle = 'rgb(0,0,0,1)'; // 改变填充颜色为蓝色
        ctx.beginPath();

        // 绘制正方形的顶部边缘
        ctx.moveTo(startX, startY);
        ctx.lineTo(startX+squareSize_x, startY);

        // 绘制正方形的底部边缘
        ctx.moveTo(startX, startY + squareSize_y);
        ctx.lineTo(startX + squareSize_x, startY + squareSize_y);

        // 执行描边
        ctx.stroke()
        // 绘制右侧的半圆
        ctx.beginPath();
        ctx.fillStyle = blank_color; // 改变填充颜色为蓝色
        ctx.arc(startX + squareSize_x, startY + radius, radius, 1.5 * Math.PI, 0.5 * Math.PI);
        ctx.fill();
        ctx.fillStyle = 'rgb(0,0,0,1)'; // 改变填充颜色为蓝色
        ctx.stroke(); // 绘制半圆的描边
    }

    fill_text_life_power(ctx,startX,startY){
        ctx.save();
        
        ctx.font = '90px Georgia';
        ctx.fillStyle = 'black';
       
        ctx.fillText(`${this.Damage}/${this.Life}`, startX, startY);
        ctx.restore();
    }

    attack_to_prepared(target_position,changed_state,attacted_obj,state_attacted_obj){//target_position[x,y,z]  撞一下然后返回原来的位置
        super.attack_to_prepared(target_position)
        console.log(changed_state)
    }
    attack_to(target_position,changed_state,attacted_obj,state_attacted_obj){//target_position[x,y,z]  撞一下然后返回原来的位置
        super.attack_to(target_position)
    }
    attack_to_finish(target_position,changed_state,attacted_obj,state_attacted_obj){//state_attacted_obj[power,life] or [life] for player
        super.attack_to_finish(target_position)
        console.log(changed_state)
        const [power,life]=changed_state
        this.Life=life
        this.Damage=power

        this.mode="none"
        
        if (attacted_obj instanceof Player){
            const ring=attacted_obj.player_life_ring
            ring.animate_set(state_attacted_obj[0],ring.life)
        }
        else if (attacted_obj instanceof Creature_Battle){
            attacted_obj.mode="none"
            attacted_obj.change_state(...state_attacted_obj)
            attacted_obj.moving_cache.push(["rotate_to_point",[90]])
            // Life=state_attacted_obj[1]
            // attacted_obj.Damage=state_attacted_obj[0]
        }
        
        
        
    }

    
    move_to_flying_prepared(target_position){
        
        const [unitVector,distance]=this.calculate_vector_move(target_position)
        this.min_distance_difference=distance;
        console.log(distance)
        const a=math.sqrt(distance*2/math.pi)
        const time_consume=1/distance+2
        
        this.moving_store=[a,unitVector,time_consume,target_position]
        this.check_distance_to_target(target_position)
    }
    move_to_flying(target_position){//target_position[x,y]
        const a=this.moving_store[0];
        const unitVector=this.moving_store[1];
        const time_consume=this.moving_store[2];
        //console.log(time_consume)
        const x=(a*math.pi/100)*this.moving_precentage
        const vel=a*Math.pow(Math.sin(x/a),2)/((100/(TIME_INTERVAL*time_consume))/(a*math.pi))
        const new_vel=math.multiply(vel,unitVector)
        const new_pos=math.add(this.position,new_vel);
        this.position[0]=new_pos[0]
        this.position[1]=new_pos[1]
        this.position[2]=new_pos[2]
        this.moving_precentage+=TIME_INTERVAL*time_consume
        this.check_distance_to_target(target_position)
        console.log(this.position,target_position,this.calculate_vector_move(target_position),this.moving_precentage,this.min_distance_difference)
        
    }
    move_to_flying_finish(target_position){
        const final_pos=this.moving_store[3];
        this.position[0]=final_pos[0]
        this.position[1]=final_pos[1]
        this.position[2]=final_pos[2]

        this.accurate_position[1]=final_pos[1]
        this.move_to_fly_flag=this.flying
        if (this.move_to_fly_flag){
            this.flying_x=0
        }
        
        this.pick_moving_function()
        
    }

    check_flying(){
        if (this.current_flying!=this.flying){
            this.current_flying=this.flying
            if(this.flying){
                this.moving_cache.push(["move_to_flying",[[this.accurate_position[0],this.flying_height,this.accurate_position[2]]]])
            }
            else{

                this.moving_cache.push(["move_to_flying",[[this.accurate_position[0],this.unflying_height,this.accurate_position[2]]]])
            }
        }
    }

    flying_motion(){
        if(this.flying && !this.moving && this.move_to_fly_flag){
            this.flying_x+=Math.PI/64
            this.accurate_position[1]+=Math.sin(this.flying_x)*0.05;
            this.position[1]=this.accurate_position[1]

        }
    }

    change_state(Damage,Life){
        this.Damage=Damage
        this.Life=Life
        this.card.Damage=Damage
        this.card.Life=Life
    }

}


class Land_Battle extends Card_Battle {
    constructor(width,height,position,size,card,player,table){
        super(width,height,position,size,card,player,table)
        this.type="Land";
        this.manas=card.manas

    }
    
}


