class Creature_Battle extends Card_Battle {
    constructor(width,height,position,size,card,player){
        super(width,height,position,size,card,player)
        // this.Org_Life=card.Org_Life;
        // this.Life=card.Life;
        // this.Org_Damage=card.Org_Damage;
        // this.Damage=card.Damage;
        this.Org_Life=1;
        this.Life=20;
        this.Org_Damage=1;
        this.Damage=20;
        this.type="Creature";
        
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

}


class Land_Battle extends Card_Battle {
    constructor(width,height,position,size,card,player){
        super(width,height,position,size,card,player)
        this.type="Land";

    }
    
}


