class Creature_Hand extends Card_Hand {
    constructor(width,height,position,size,dynamic_canvas,color_fee,Life,Damage,name,id,player){
        super(width,height,position,size,dynamic_canvas,color_fee,name,id,player)
        this.Org_Life=Life;
        this.Life=Life;
        this.Org_Damage=Damage;
        this.Damage=Damage;
        this.type="Creature";
        
    }

    
    update(){
        super.update();
        this.print_life_damage();
        

        
    }
    print_life_damage(){
        this.create_blank_space(
            this.dynamic_canvas[0],
            this.dynamic_canvas[1],
            this.dynamic_canvas[0].width*6/8,
            this.dynamic_canvas[0].height*1/25
            )
        this.fill_text_life_power(
            this.dynamic_canvas[1],
            this.dynamic_canvas[0].width*6/8,
            this.dynamic_canvas[0].height*7/8
        );
    }
    create_blank_space(canvas,ctx,startX,startY){
        const blank_color="rgb(233,233,233,0.9)"
        const squareSize_x = canvas.width*1/8; // 正方形的边长
        const squareSize_y = 35;
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
        ctx.setTransform(1, 0, 0, -1, 
            0,
            525);
        ctx.font = '20px Georgia';
        ctx.fillStyle = 'black';
       
        ctx.fillText(`${this.Damage}/${this.Life}`, startX, startY);
        ctx.restore();
    }

    get_copy(){
        const card=new Creature_Hand(4,5.62,[0,0,0],2,this.dynamic_canvas,this.color_fee,this.Org_Life,this.Org_Damage,this.name,this.id,this.player)
        card.battle=this.battle
        console.log(card.battle)
        return card
    }

}


class Land_Hand extends Card_Hand {
    constructor(width,height,position,size,dynamic_canvas,name,id,player){
        super(width,height,position,size,dynamic_canvas,"",name,id,player)
        this.type="Land";

    }
    create_fee(ctx,fee_text,color_less,red,blue,green,gold,black){
    }

    get_copy(){
        const card=new Land_Hand(4,5.62,[0,0,0],2,this.dynamic_canvas,this.color_fee,this.name,this.id,this.player)
        card.battle=this.battle
        
        return card
    }
}


class Sorcery_Hand extends Card_Hand {
    constructor(width,height,position,size,dynamic_canvas,color_fee,name,id,player){
        super(width,height,position,size,dynamic_canvas,color_fee,name,id,player)
        this.type="Sorcery";
    }
    get_copy(){
        const card=new Sorcery_Hand(4,5.62,[0,0,0],2,this.dynamic_canvas,this.color_fee,this.name,this.id,this.player)
        return card
    }
}


class Instant_Hand extends Card_Hand {
    constructor(width,height,position,size,dynamic_canvas,color_fee,name,id,player){
        super(width,height,position,size,dynamic_canvas,color_fee,name,id,player);
        this.type="Instant";
    }
    get_copy(){
        const card=new Instant_Hand(4,5.62,[0,0,0],2,this.dynamic_canvas,this.color_fee,this.name,this.id,this.player)
        return card
    }

}