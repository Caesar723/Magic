class Mana_Bar{
    constructor(){
        this.position=[0,0]

        this.colors={
            'U':'rgb(170,218,250)',
            'W':'rgb(231,231,231)',
            'B':'rgb(31,31,31)',
            'R':'rgb(226,82,55)',
            'G':'rgb(135,197,149)',

        }
        this.bars={}

        let index = 0;
        for(let color in this.colors){
            const bar=new Color_Bar([1470-5*150,index*15-20],this.colors[color])
            index++
            this.bars[color]=bar
        }
        

        //this.manas=[0,0,0,0,0]//

    }
    update(){
        for(let color in this.bars){
            this.bars[color].update()
        }
    }
    draw(canvas,ctx,camera){
        for(let color in this.bars){
            this.bars[color].draw(canvas,ctx,camera)
        }
    }

    set_mana(manas){//list of mana[blue,white,black,red,green]
        let index=0;
        for (let color in this.bars){
            this.bars[color].animate_set(manas[index])
            console.log()
            index++
        }
    }
    check_finish(){
        
        for(let color in this.bars){
            if (this.bars[color].moving==true){
                return false
            }
        }
        return true
    }

    
}
class Color_Bar{
    constructor(position,color){
        this.position=position
        this.color=color
        this.val=0
        const width=5
        const height=1
        this.canvas=document.createElement('canvas');
        this.canvas.width=width*150
        this.canvas.height=height*80
        this.ctx=this.canvas.getContext('2d')
        this.interval=2
        this.moving=false
    }
    animate_set(val){
        this.moving_precentage=0
        const different=val-this.val
        this.min_distance_difference=math.abs(different)
        const unit=(different/math.abs(different))
        const a=math.sqrt(math.abs(different)*2/math.pi)
        this.moving_store=[a,val,unit]
        this.moving=true
    }
    animate_move(){
        const a=this.moving_store[0];
        const unit=this.moving_store[2];
        const x=(a*math.pi/100)*this.moving_precentage
        const vel=unit*a*Math.pow(Math.sin(x/a),2)/((100/(this.interval))/(a*math.pi))
        this.moving_precentage+=this.interval*TIME_INTERVAL/2
        return vel
    }
    check_move(){
        //console.log(this.moving)
        if (this.moving){
            this.val+=this.animate_move()
            this.check_distance()

        }
    }
    check_distance(){
        const val=this.moving_store[1]
        const difference=math.abs(val-this.val)
        if (difference<=this.min_distance_difference && this.moving_precentage<100){
            this.min_distance_difference=difference
        }
        else{
            console.log(1)
            this.moving=false
            this.val=val
        }
    }

    draw(canvas,ctx,camera){
        ctx.drawImage(this.canvas,this.position[0],this.position[1])
    }
    update(){
        this.check_move()
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        this.print_bar(this.canvas,this.ctx)
        this.print_text(this.canvas,this.ctx)
    }
    print_bar(canvas,ctx){
        const X = canvas.width -70;
        const centerY = canvas.height / 2;
        const length=this.val*30
        //console.log(this.color)
        ctx.beginPath();
        
        ctx.shadowBlur = 5;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;
        ctx.shadowColor = this.color;
        ctx.lineWidth = 6; // 设置进度条的宽度
        ctx.lineCap = 'round';
        ctx.strokeStyle = this.color; 
        ctx.moveTo(X, centerY);
        // 线段终点
        ctx.lineTo(X-length, centerY);
        ctx.stroke();
    }
    print_text(canvas,ctx){
        const X = canvas.width -50;
        const centerY = canvas.height / 2;
        ctx.font = '15px Cinzel';
        ctx.fillStyle = "rgb(231,231,231)";
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(Math.round(this.val) + '', X, centerY);

    }
}