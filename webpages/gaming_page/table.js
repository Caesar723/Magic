var TIME_INTERVAL=2


class Table{
    constructor(){
        this.canvas = document.getElementById("myCanvas");
        this.ctx = this.canvas.getContext("2d");
        this.canvas.width = 1470;
        this.canvas.height = 742;
        this.time_interval=0.02//每隔0.02秒进行一次刷新
        this.table_graph=new Table_graph(2,1,1,[0,0,0],20,"webpages/image_source/game/background.jpg");
        
        // this.camera=new Camera([0,-30,-7*0.7])
        // this.camera.angle_y=1.34
        this.camera=new Camera([0,-60,-7*0.7])
        this.camera.angle_y=1.34
        this.camera.angle_x=0

        this.card_frame=new Card_frame()
        this.opponent_battlefield=[]
        this.self_battlefield=[]
        this.opponent_battlefield_delete=[]
        this.self_battlefield_delete=[]


        ///
        for (let i=0;i<1;i++){
            const canvas=this.card_frame.generate_card("blue","Caesar","creature","Common","shausoaishaisuhai","cards/creature/Angelic Protector/image.jpg")
            const card=new Creature_Hand(4,5.62,[0,0,60],1.6,canvas,"3U","Caesar",1122334455)
            const card_battle=new Creature_Battle(6,5,[-25+i*5,-20,0],0.3,card,"self",this)
            this.self_battlefield.push(card_battle)
        }
        ////
        
        
    }

    arrange_cards_battle(arr,unit){//1:self,-1:opponent
        const card_len=6
        const max_len=11
        const level = Math.ceil(arr.length / max_len);
        const gap_max=2
        const gap_min=1.4
        const max_size=0.6
        const min_size=0.3

        var length=arr.length
        if (arr.length>max_len){
            length=max_len
        }
        const gap=gap_max-length*((gap_max-gap_min)/max_len)
        const size=max_size-length*((max_size-min_size)/max_len)
        const dis_between=card_len*size*2*gap
        
        for (let layer=0;layer<level;layer++){
            if (layer==level-1 && arr.length%max_len!=0){
                //console.log(1)
                const start_point=-dis_between*((arr.length%max_len)-1)/2
                for (let i =layer*max_len;i<layer*max_len+(arr.length%max_len);i++){
                    const position=[start_point+(i-layer*max_len)*dis_between,arr[i].accurate_position[1],(-5-layer*5)*unit]
                    arr[i].accurate_position=position
                    
                    arr[i].start_moving("move_to",[position])
                    arr[i].change_size(size)
                    
                }
            }
            else{
                //console.log(2)
                const start_point=-dis_between*(length-1)/2
                for (let i =layer*max_len;i<layer*max_len+max_len;i++){
                    const position=[start_point+(i-layer*max_len)*dis_between,arr[i].accurate_position[1],(-5-layer*5)*unit]
                    arr[i].accurate_position=position
                    
                    arr[i].start_moving("move_to",[position])
                    arr[i].change_size(size)
                    
                }
            }
        }
        

    }

    update(){
        this.arrange_cards_battle(this.self_battlefield,1)
        this.arrange_cards_battle(this.opponent_battlefield,-1)
        this.table_graph.update(this.camera)
        
        for (let i_self in this.self_battlefield){
            
            this.self_battlefield[i_self].update(this.camera)
        }
        for (let i_oppo in this.opponent_battlefield){
            
            this.opponent_battlefield[i_oppo].update(this.camera)
        }
        
        this.self_battlefield= this.self_battlefield.filter(item => !(this.self_battlefield_delete.includes(item)))
        this.opponent_battlefield=this.opponent_battlefield.filter(item => !(this.opponent_battlefield_delete.includes(item)))
        
        this.self_battlefield_delete=[]
        this.opponent_battlefield_delete=[]
        
        
    }
    
    draw(){//先画背景再画影子最后画图片
        this.table_graph.draw(this.camera,this.canvas,this.ctx)
        
        for (let i_self in this.self_battlefield){
            //this.ctx.drawImage(this.self_battlefield[i_self_battlefield].canvas,100,100,this.self_battlefield[i_self_battlefield].canvas.width,this.self_battlefield[i_self_battlefield].canvas.height)
            this.self_battlefield[i_self].draw_shade(-20,this.camera,this.ctx,this.canvas)
            
        }
        for (let i_oppo in this.opponent_battlefield){
            //this.ctx.drawImage(this.self_battlefield[i_self_battlefield].canvas,100,100,this.self_battlefield[i_self_battlefield].canvas.width,this.self_battlefield[i_self_battlefield].canvas.height)
            this.opponent_battlefield[i_oppo].draw_shade(-20,this.camera,this.ctx,this.canvas)
            
        }
        for (let i_self in this.self_battlefield){
            
            this.self_battlefield[i_self].draw(this.camera,this.ctx,this.canvas)
            
        }
        for (let i_oppo in this.opponent_battlefield){
            //this.opponent_battlefield[i_oppo].draw_shade(-20,this.camera,this.ctx,this.canvas)
            //this.ctx.drawImage(this.self_battlefield[i_self_battlefield].canvas,100,100,this.self_battlefield[i_self_battlefield].canvas.width,this.self_battlefield[i_self_battlefield].canvas.height)
            this.opponent_battlefield[i_oppo].draw(this.camera,this.ctx,this.canvas)
            // this.self_battlefield[i_self_battlefield].angle_x=this.self_battlefield[i_self_battlefield].angle_x+0.01
            // this.self_battlefield[i_self_battlefield].position[0]=this.self_battlefield[i_self_battlefield].position[0]+0.01
        }
    }

    draw_table(){

    }
}