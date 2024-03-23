var TIME_INTERVAL=2


class Table{
    constructor(){
        this.canvas = document.getElementById("myCanvas");
        this.ctx = this.canvas.getContext("2d");
        this.canvas.width = 1470;
        this.canvas.height = 742;
        this.time_interval=0.02//每隔0.02秒进行一次刷新
        this.table_graph=new Table_graph(2,1,1,[0,0,5],20,"webpages/image_source/game/background.jpg");
        
        // this.camera=new Camera([0,-30,-7*0.7])
        // this.camera.angle_y=1.34
        this.camera=new Camera([0,0,-17])
        this.camera.angle_y=0
        this.camera.angle_x=0

        this.card_frame=new Card_frame()
        const canvas=this.card_frame.generate_card("blue","Caesar","creature","Common","shausoaishaisuhai","cards/creature/Angelic Protector/image.jpg")
        const card=new Creature_Hand(4,5.62,[0,0,60],1.6,canvas,"3U","Caesar",1122334455)
        const card_battle=new Creature_Battle(6,5,[0,-20,0],0.6,card)

        
        this.opponent_battlefield=[]
        this.self_battlefield=[card_battle]
    }
    update(){
        this.table_graph.update(this.camera)
        

        for (let i_self_battlefield in this.self_battlefield){
            
            this.self_battlefield[i_self_battlefield].update(this.camera)
        }
        
        
    }
    draw(){//先画背景再画影子最后画图片
        this.table_graph.draw(this.camera,this.canvas,this.ctx)
        
        for (let i_self_battlefield in this.self_battlefield){
            //this.ctx.drawImage(this.self_battlefield[i_self_battlefield].canvas,100,100,this.self_battlefield[i_self_battlefield].canvas.width,this.self_battlefield[i_self_battlefield].canvas.height)
            this.self_battlefield[i_self_battlefield].draw_shade(-20,this.camera,this.ctx,this.canvas)
        }
        for (let i_self_battlefield in this.self_battlefield){
            //this.ctx.drawImage(this.self_battlefield[i_self_battlefield].canvas,100,100,this.self_battlefield[i_self_battlefield].canvas.width,this.self_battlefield[i_self_battlefield].canvas.height)
            this.self_battlefield[i_self_battlefield].draw(this.camera,this.ctx,this.canvas)
            // this.self_battlefield[i_self_battlefield].angle_x=this.self_battlefield[i_self_battlefield].angle_x+0.01
            // this.self_battlefield[i_self_battlefield].position[0]=this.self_battlefield[i_self_battlefield].position[0]+0.01
        }
    }

    draw_table(){

    }
}