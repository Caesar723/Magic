class Buttons{
    //每一个button 必须要有click，find_button_by_mouse函数


    constructor(client){
        this.auto_pass=new Button_Auto_Pass(client)
    }

    update(){
        this.auto_pass.update()
    }

    draw(canvas,ctx){
        
        this.auto_pass.draw(canvas,ctx)
        

    }
    find_button_by_mouse(mouse_pos){

      if (this.auto_pass.find_button_by_mouse(mouse_pos)){
        return this.auto_pass
      }
      return undefined
    }
}






class Button_Auto_Pass{

    constructor(client){
        this.flag=false
        this.client=client



        this.width=100
        this.height=25
        this.x=1330
        this.y=100
        this.changing_color=false
        this.changing_precentage=0
        this.color_press=[224, 103, 78] // 按下去时红色
        this.color_unpress=[255,223,56] // 没有按是黄色
        this.current_color=[255,223,56] 
        this.min_difference=[0,0,0]
        this.content="Auto Pass >>"

        
    }
    check_target(colors){
        const dif_r=math.abs(colors[0]-this.current_color[0])
        const dif_g=math.abs(colors[1]-this.current_color[1])
        const dif_b=math.abs(colors[2]-this.current_color[2])
        
        if (dif_r<=this.min_difference[0] && dif_g<=this.min_difference[1] && dif_b<=this.min_difference[2]  && this.changing_precentage<100){
            this.min_difference=[dif_r,dif_g,dif_b]
        }
        else{
            this.color_change_finish()
        }
    }
    print_text(canvas,ctx){
        const color=this.get_current_color()
        
        ctx.font = '15px Cinzel';
        ctx.fillStyle = color;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.content, this.x+this.width/2-5, this.y+this.height/2);
    }
    color_change_prepared(colors){
      //console.log(colors,this.current_color)
      const dif_r=math.abs(colors[0]-this.current_color[0])
      const dif_g=math.abs(colors[1]-this.current_color[1])
      const dif_b=math.abs(colors[2]-this.current_color[2])

      const unit_r=dif_r/(colors[0]-this.current_color[0])
      const unit_g=dif_g/(colors[1]-this.current_color[1])
      const unit_b=dif_b/(colors[2]-this.current_color[2])

      const a_r=math.sqrt(dif_r*2/math.pi)
      const a_g=math.sqrt(dif_g*2/math.pi)
      const a_b=math.sqrt(dif_b*2/math.pi)

      this.changing_store=[a_r,a_g,a_b,unit_r,unit_g,unit_b,colors]

      this.min_difference=[dif_r,dif_g,dif_b]

      this.changing_color=true
      this.changing_precentage=0
      this.check_target(colors)
    }
    color_change(){
      const time_consume=5
      const a_r= this.changing_store[0]
      const a_g= this.changing_store[1]
      const a_b= this.changing_store[2]
      const unit_r= this.changing_store[3]
      const unit_g= this.changing_store[4]
      const unit_b= this.changing_store[5]
      const x_r=(a_r*math.pi/100)*this.changing_precentage
      const x_g=(a_g*math.pi/100)*this.changing_precentage
      const x_b=(a_b*math.pi/100)*this.changing_precentage

      const dif_r=unit_r*a_r*Math.pow(Math.sin(x_r/a_r),2)/((100/(time_consume))/(a_r*math.pi))
      const dif_g=unit_g*a_g*Math.pow(Math.sin(x_g/a_g),2)/((100/(time_consume))/(a_g*math.pi))
      const dif_b=unit_b*a_b*Math.pow(Math.sin(x_b/a_b),2)/((100/(time_consume))/(a_b*math.pi))

      this.current_color[0]+=dif_r
      this.current_color[1]+=dif_g
      this.current_color[2]+=dif_b
      //console.log(this.current_color,a_r,a_g,a_b)
      this.changing_precentage+=time_consume*TIME_INTERVAL/2
      this.check_target(this.changing_store[6])
    }
    color_change_finish(){
        this.current_color=[...this.changing_store[6]]
        this.changing_color=false
        this.changing_precentage=0
        //console.log(this.current_color)
    }
    change_red(){
        this.color_change_prepared(this.color_press)
    }
    change_yellow(){
        this.color_change_prepared(this.color_unpress)
    }

    update(){
      if (this.changing_color){
        this.color_change()
      }

    }
    draw(canvas,ctx){
      // 清除canvas
      ctx.save()
      

      

      // 计算按钮各部分的尺寸和位置
      const rectWidth = this.width * 0.8;
      const circleRadius = this.height / 2;
      const circleCenter = this.x + rectWidth;

      // 绘制左侧长方形
      ctx.beginPath();
      const color=this.get_current_color()
      ctx.strokeStyle = color;
      ctx.lineWidth = 4; // 设置进度条的宽度
      ctx.lineCap = 'round';
      ctx.shadowColor = color; // 半透明的蓝色光晕
        // 设置阴影的模糊级别
      ctx.shadowBlur = 20;
      ctx.shadowOffsetX = 0;
      ctx.shadowOffsetY = 0;
      ctx.moveTo(this.x + rectWidth, this.y);
      ctx.lineTo(this.x, this.y);
      ctx.lineTo(this.x, this.y + this.height);
      ctx.lineTo(this.x + rectWidth, this.y + this.height);
      ctx.stroke(); // 使用stroke()方法绘制边框
      ctx.closePath();
 

      // 绘制右侧半圆边框
      ctx.beginPath();
      ctx.arc(circleCenter, this.y + this.height / 2, circleRadius, Math.PI * 1.5, Math.PI / 2);
      ctx.stroke(); // 使用stroke()方法绘制边框

      ctx.restore()

      this.print_text(canvas,ctx)

    }

    get_current_color(){
      return `rgb(${this.current_color[0]}, ${this.current_color[1]}, ${this.current_color[2]})`;
    }
    find_button_by_mouse(mouse_pos){

      if (this.x<mouse_pos[0] && this.x+this.width>mouse_pos[0] && this.y<mouse_pos[1] && this.y+this.height>mouse_pos[1]){


        return true
      }
      return false
    }
    click(){
      if (this.flag){
        var values = [this.client.self_player.name,'auto_passing',"false"];
        //this.end()
      }
      else{
        var values = [this.client.self_player.name,'auto_passing',"true"];
        //this.start()
      }
      this.client.socket_main.send(values.join('|'));
    }

    start(){
      this.flag=true
      this.change_red()
    }

    end(){
      this.flag=false
      this.change_yellow()
    }

    
        
    
}