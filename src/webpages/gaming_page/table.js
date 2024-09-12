


class Table{
    constructor(client){
        this.client=client
        this.canvas = document.getElementById("myCanvas");//new OffscreenCanvas(200, 200);
        this.canvas.width = 1470;
        this.canvas.height = 742;

        //this.canvas =this.canvas.transferControlToOffscreen();
        this.ctx = this.canvas.getContext("2d");
        this.time_interval=0.02//每隔0.02秒进行一次刷新
        this.table_graph=new Table_graph(2,1,1,[0,0,0],20,"webpages/image_source/game/background.jpg");
        this.deck_self_graph=new Deck_battle(4,2,5.62,[-28.5,-20-3,-15],0.5,"webpages/image_source/card/back.png")
        this.deck_oppo_graph=new Deck_battle(4,2,5.62,[28.5,-20-3,+15],0.5,"webpages/image_source/card/back.png")
        this.timmer_turn=new Timmer(120,[34,-22,0],4,'turn')
        this.timmer_bullet=new Timmer(10,[-34,-22,0],4,'bullet')
        this.special_effects=new SpecialEffects()
        this.deck_oppo_graph.angle_y=Math.PI
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

        this.opponent_landfield=[]
        this.self_landfield=[]
        this.opponent_landfield_delete=[]
        this.self_landfield_delete=[]


        ///
        // for (let i=0;i<1;i++){
        //     const canvas=this.card_frame.generate_card("blue","Caesa","creature","Common","shausoaishaisuhai","cards/creature/Angelic Protector/image.jpg")
        //     const card=new Creature_Hand(4,5.62,[0,0,60],1.6,canvas,"3U",20,20,20,20,"Caesa",1122334455)
        //     const card_battle=new Creature_Battle(6,5,[-25+i*5,-20,0],0.3,card,"self",this)
        //     this.self_battlefield.push(card_battle)
        // }
        ////
        
        
    }
    set_player(player_self,player_oppo){
        this.player_self=player_self
        this.player_oppo=player_oppo
        this.player_self.table=this
        this.player_oppo.table=this

        player_self.oppo=player_oppo
        player_oppo.oppo=player_self

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
    arrange_cards_land(arr,unit){
        const grouped_items=this.groupValues(arr)
        //console.log(grouped_items)
        const card_len=6
        const start_point=-20
        
        const size=0.3

        const gap=1.5
        const dis_between=card_len*size*2*gap


        const small_distance=0.2
        for (let grouped_index in grouped_items){
            for (let offset in grouped_items[grouped_index]){
                const card=grouped_items[grouped_index][offset]
                const position=[
                    (start_point+dis_between*grouped_index+small_distance*offset)*unit,
                    card.accurate_position[1],
                    (-13+offset*small_distance)*unit

                ]
                card.accurate_position=position
                card.start_moving("move_to",[position])
                card.change_size(size)
            }
        }
    }
    groupValues(arr) {
        const groups = {};
        arr.forEach(item => {
            if (!groups[item.card.name]) {
                groups[item.card.name] = [];
            }
            groups[item.card.name].push(item);
        });
        
        for (const groupName in groups) {
            groups[groupName].sort((a, b) => a.z_index - b.z_index);
        }
        //console.log(groups)
        return Object.values(groups);  // 返回一个包含所有组的数组
    }
    
    // const myArray = [1, 2, 2, 3, 4, 4, 4, 5];
    // const grouped = groupValues(myArray);
    // console.log(grouped);  /

    update(){
        
        this.table_graph.update(this.camera)
        this.timmer_turn.update(this.camera)
        this.timmer_bullet.update(this.camera)

        this.player_self.player_life_ring.update(this.camera)
        this.player_oppo.player_life_ring.update(this.camera)

        this.deck_self_graph.update(this.camera)
        this.deck_oppo_graph.update(this.camera)
        //battle
        
        this.arrange_cards_battle(this.self_battlefield,1)
        this.arrange_cards_battle(this.opponent_battlefield,-1)
        this.arrange_cards_land(this.self_landfield,1)
        this.arrange_cards_land(this.opponent_landfield,-1)
        for (let i_self in this.self_battlefield){
            
            this.self_battlefield[i_self].update(this.camera)
        }
        for (let i_oppo in this.opponent_battlefield){
            
            this.opponent_battlefield[i_oppo].update(this.camera)
        }
        //land
        for (let i_self in this.self_landfield){
            
            this.self_landfield[i_self].update(this.camera)
        }
        for (let i_oppo in this.opponent_landfield){
            
            this.opponent_landfield[i_oppo].update(this.camera)
        }
        
        

        
        
        this.self_battlefield= this.self_battlefield.filter(item => !(this.self_battlefield_delete.includes(item)))
        this.opponent_battlefield=this.opponent_battlefield.filter(item => !(this.opponent_battlefield_delete.includes(item)))
        
        this.self_battlefield_delete=[]
        this.opponent_battlefield_delete=[]


        this.self_landfield= this.self_landfield.filter(item => !(this.self_landfield_delete.includes(item)))
        this.opponent_landfield=this.opponent_landfield.filter(item => !(this.opponent_landfield_delete.includes(item)))
        

        this.opponent_landfield_delete=[]
        this.self_landfield_delete=[]

        this.special_effects.update(this.camera)

        //this.sort_cards()
        
        
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



        const combinedArray = this.self_battlefield.concat(
            this.opponent_battlefield, 
            this.opponent_landfield,
            this.self_landfield,
            );
        combinedArray.sort((a, b) =>{
            const positionDiff = b.position[1] - a.position[1];
            if (positionDiff !== 0) {
                // 如果 position[1] 不相等，直接返回差值
                return positionDiff;
            } else {
                // 如果 position[1] 相等，按照 z-index 排序
                return a.z_index - b.z_index;
            }});

        for (let card_i in combinedArray){
            combinedArray[card_i].draw(this.camera,this.ctx,this.canvas)
        }

        // for (let i_self in this.self_battlefield){
            
        //     this.self_battlefield[i_self].draw(this.camera,this.ctx,this.canvas)
            
        // }
        // for (let i_oppo in this.opponent_battlefield){
        //     //this.opponent_battlefield[i_oppo].draw_shade(-20,this.camera,this.ctx,this.canvas)
        //     //this.ctx.drawImage(this.self_battlefield[i_self_battlefield].canvas,100,100,this.self_battlefield[i_self_battlefield].canvas.width,this.self_battlefield[i_self_battlefield].canvas.height)
        //     this.opponent_battlefield[i_oppo].draw(this.camera,this.ctx,this.canvas)
        //     // this.self_battlefield[i_self_battlefield].angle_x=this.self_battlefield[i_self_battlefield].angle_x+0.01
        //     // this.self_battlefield[i_self_battlefield].position[0]=this.self_battlefield[i_self_battlefield].position[0]+0.01
        // }
        // //land
        // for (let i_self in this.self_landfield){
        //     this.self_landfield[i_self].draw(this.camera,this.ctx,this.canvas)
        // }
        // for (let i_oppo in this.opponent_landfield){
        //     this.opponent_landfield[i_oppo].draw(this.camera,this.ctx,this.canvas)
        // }

        this.deck_self_graph.draw(this.camera,this.canvas,this.ctx)
        this.deck_oppo_graph.draw(this.camera,this.canvas,this.ctx)
        this.timmer_turn.draw(this.camera,this.ctx,this.canvas)
        this.timmer_bullet.draw(this.camera,this.ctx,this.canvas)
        this.player_self.player_life_ring.draw(this.camera,this.ctx,this.canvas)
        this.player_oppo.player_life_ring.draw(this.camera,this.ctx,this.canvas)
        this.special_effects.draw(this.camera,this.ctx,this.canvas)

    }

    draw_player(){

    }
    draw_deck(){

    }
    sort_cards(){

        this.self_battlefield.sort(function(a, b) {
            return a.z_index - b.z_index;
        });
        this.opponent_battlefield.sort(function(a, b) {
            return a.z_index - b.z_index;
        });


        this.opponent_landfield.sort(function(a, b) {
            return a.z_index - b.z_index;
        });
        this.self_landfield.sort(function(a, b) {
            return a.z_index - b.z_index;
        });
    }

    get_self_battlefield(){
        return this.self_battlefield
    }
    get_opponent_battlefield(){
        return this.opponent_battlefield
    }

    get_self_landfield(){
        return this.self_landfield
    }

    get_opponent_landfield(){
        return this.opponent_landfield
    }
}