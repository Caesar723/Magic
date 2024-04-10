class Action_Bar{

    constructor(){





        this.actions=[]
        this.position=[0,0]
        this.target_position_hide=-90
        this.target_position_show=0

        this.canvas=document.createElement('canvas');
        this.canvas.width = 177*(742/807);
        this.canvas.height = 742;
        this.ctx=this.canvas.getContext('2d')

        this.back_img=new Image();
        this.back_img.src="webpages/gaming_page/bar.jpg";

        this.arrow_img=new Image();
        this.arrow_img.src="webpages/gaming_page/arrow.png";




        this.mode="hide"//show hide
        this.card_mode="hide"
        this.action_showed=undefined
        this.moving=false

        

    }
    set_image(){
        for (let i in this.actions){
            this.actions[i].arrow_img=this.arrow_img
        }
    }
    update_graph(){
        this.ctx.save()
        this.draw_rect_smooth(this.ctx,0,0,this.canvas.width,this.canvas.height)
        
        this.ctx.drawImage(this.back_img,0,0,this.canvas.width,this.canvas.height)
        this.ctx.restore()
        // this.ctx.beginPath();
        // this.ctx.moveTo(0, 0);
        // this.ctx.bezierCurveTo(0, 100, 150, 100, 150, 50);
        // this.ctx.bezierCurveTo(150, 100, 150, 150, 100, 150);
        // this.ctx.bezierCurveTo(150, 150, 50, 150, 50, 100);
        // this.ctx.bezierCurveTo(50, 100, 50, 50, 100, 50);
        // this.ctx.clip();
    }
    update(){
        this.update_position()
        if (this.mode=="show"){

        
            
            this.ctx.clearRect(0,0,this.canvas.width,this.canvas.height)
            this.set_image()
            this.update_graph()
            const len=this.actions.length

            var last_index=this.actions.length
            if (last_index>11){
                last_index=11
            }
            for (let i =0;i<last_index;i++){
                const index=len-i-1
                //console.log(i,index)
                
                this.actions[index].draw_image(this.ctx,i)
            }


            if (this.card_mode=="show"){
                this.action_showed.update_cards()
            }
        }
    }
    draw(canvas,ctx,camera){

        ctx.drawImage(this.canvas,this.position[0]-70,0)

        //console.log(this.showed_action)
        this.showed_action(ctx,canvas,camera)
    }

    check_move(){
        if (this.moving){
            if (this.mode=="hide" && this.position[0]<=this.target_position_hide){
                this.moving=false
                this.position[0]=this.target_position_hide
                return true
            }
            else if(this.mode=="show" && this.position[0]>=this.target_position_show){
                this.moving=false
                this.position[0]=this.target_position_show
                return true
            }
            else{
                return false
            }
        }
        else{
            if (this.mode=="hide" && this.position[0]>this.target_position_hide){
                this.moving=true
            }
            else if(this.mode=="show" && this.position[0]<this.target_position_show){
                this.moving=true
            }
            return false
        }
    }
    update_position(){
        //console.log(this.mode)
        this.check_move()
        if (this.moving){
            if (this.mode=="hide"){
                this.position[0]=this.position[0]-8
            }
            else if(this.mode=="show"){
                this.position[0]=this.position[0]+8
            }
        }
    }

    check_mouse(mouse_pos){
        
        if (mouse_pos[0]<(this.canvas.width-70)){
            this.mode="show"//show hide
        }
        else{
            this.mode="hide"//show hide
        }
        
        if (mouse_pos[0]<(this.canvas.width+this.position[0]-70)){
            
            console.log(this.mode)
            const len=this.actions.length
            for (let i in this.actions){
                const index=len-i-1
                const result=this.actions[index].check_mouse(mouse_pos,i)
                if (result){
                    return this.actions[index]
                }
            }
            return false
        }
        else{
            
            return false
        }
    }
    draw_rect_smooth(ctx,x,y,width,height){
        
        
        var radius = 40; // 圆角半径

        // 绘制圆角长方形路径
        ctx.beginPath();
        ctx.moveTo(x + radius, y);
        ctx.lineTo(x + width - radius, y);
        ctx.arcTo(x + width, y, x + width, y + radius, radius);
        ctx.lineTo(x + width, y + height - radius);
        ctx.arcTo(x + width, y + height, x + width - radius, y + height, radius);
        ctx.lineTo(x + radius, y + height);
        ctx.arcTo(x, y + height, x, y + height - radius, radius);
        ctx.lineTo(x, y + radius);
        ctx.arcTo(x, y, x + radius, y, radius);
        ctx.closePath();
        // 应用裁剪
        ctx.clip();
    }

    showed_action(ctx,canvas,camera){
        if (this.card_mode=="show"){
            this.action_showed.draw_action(ctx,canvas,camera)
        }
    }

}