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
        this.flying=false//trur-> flying
        
    }

    
    update(camera){
        super.update(camera);
        this.print_life_damage();
        

        
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


