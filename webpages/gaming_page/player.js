class Player{
    constructor(name,canvas,ctx){
        // this.life=20
        // this.max_life=20
        this.canvas=canvas;
        this.ctx=ctx;
        this.name=name;
        this.cards=[];
        this.camera=new Camera([0,0,-50])
        this.card_frame=new Card_frame()
    }
    initinal_all(content){

    }

    draw(){

    }
    update(){

    }
    draw_life(){

    }
}

class Opponent extends Player{
    constructor(name,canvas,ctx){
        super(name,canvas,ctx);

        const card=new Card_Hand_Oppo(4,5.62,[0,0,0],0.7,1122334455,this)
        this.cards=[card];
        this.hand_delete=[]

        this.unit=-1
        this.player_life_ring=new Player_Life([-0.47,-20,14],6,this.unit)

    }

    update(){

        this.arrange_cards()
        for (let card_i in this.cards){
            this.cards[card_i].update()

        }
        this.cards= this.cards.filter(item => !(this.hand_delete.includes(item)))
        this.hand_delete=[]
        //this.sort_cards()
    }

    draw(){
        for (let card_i in this.cards){
            this.cards[card_i].draw(this.camera,this.ctx,this.canvas)
            //console.log(this.cards[card_i].position)
            
        }
    }

    arrange_cards(){
        
        const max_angle=2*math.pi/180
        const lan_angle=15*(math.pi/180)/this.cards.length
        //console.log(lan_angle,max_angle)
        if (lan_angle>max_angle){
            var angle_between=max_angle
        }
        else{
            var angle_between=lan_angle
        }
        //var angle_between=130*(math.pi/180)/this.cards.length//2*math.pi/180
        const radius=100

        
        const start_angle=math.pi-angle_between*(this.cards.length-1)/2
        for (let card_i in this.cards){
            const position=math.multiply(rotateZ(start_angle+card_i*angle_between),math.matrix([[0],[-radius],[0]]));

            //position=math.multiply(rotateZ(-angle_between),position);
            
            const position_arr=[position.get([0,0])-20,position.get([1,0])-radius-20,position.get([2,0])]
            this.cards[card_i].start_moving("move_to",[position_arr])
            this.cards[card_i].angle_z=-start_angle-card_i*angle_between
            //this.cards[card_i].change_size(1)

            
        }
    }
}

class Self extends Player{
    constructor(name,canvas,ctx){
        super(name,canvas,ctx);

        const canvas_dynamic=this.card_frame.generate_card("blue","Caesar","creature","Common","shausoaishaisuhai","cards/creature/Angelic Protector/image.jpg")
        const card=new Creature_Hand(4,5.62,[0,0,0],1.5,canvas_dynamic,"3U",20,20,20,20,"Caesar",1122334455,this)
        

        this.cards=[card];
        this.hand_delete=[]

        this.cards_mode="ignore"//两个模式，第一个是ignore，卡牌缩小，放到右侧，第二个是focus，卡牌放大
        this.focus_size=1.5
        this.ignore_size=1

        this.unit=1
        this.player_life_ring=new Player_Life([-0.47,-20,-13],6,this.unit)

        this.mana_bar=new Mana_Bar()
    }
    get_enlarge_size(){
        if (this.cards_mode==="ignore"){
            return this.ignore_size+0.5
        }
        else{
            return this.focus_size+0.5
        }
        
    }
    get_small_size(){
        if (this.cards_mode==="ignore"){
            return this.ignore_size
        }
        else{
            return this.focus_size
        }
    }
    change_to_ignore(){
        if (this.cards_mode=="focus"){
            this.cards_mode="ignore"
            //console.log(123)
            const angle_between=3*math.pi/180
            const radius=100

            
            const start_angle=-angle_between*(this.cards.length-1)/2
            for (let card_i in this.cards){
                const position=math.multiply(rotateZ(start_angle+card_i*angle_between),math.matrix([[0],[-radius],[0]]));

                //position=math.multiply(rotateZ(-angle_between),position);
                
                const position_arr=[position.get([0,0])+20,position.get([1,0])+radius+20,position.get([2,0])]
                this.cards[card_i].start_moving("small",[position_arr])
                //this.cards[card_i].moving_cache.push(["enlarge",[position_arr]])
                this.cards[card_i].angle_z=start_angle+card_i*angle_between
            }
        }
        
        
    }
    change_to_focus(){
        if (this.cards_mode=="ignore"){
            this.cards_mode="focus"
            const angle_between=1*math.pi/180
            const radius=500

            
            const start_angle=-angle_between*(this.cards.length-1)/2
            for (let card_i in this.cards){
                const position=math.multiply(rotateZ(start_angle+card_i*angle_between),math.matrix([[0],[-radius],[0]]));

                //position=math.multiply(rotateZ(-angle_between),position);
                
                const position_arr=[position.get([0,0]),position.get([1,0])+radius+15,position.get([2,0])]
                this.cards[card_i].start_moving("enlarge",[position_arr])
                //this.cards[card_i].moving_cache.push(["enlarge",[position_arr]])
                this.cards[card_i].angle_z=start_angle+card_i*angle_between
            }
        }
        
    }
    update(){
        //console.log(this.cards)
        this.arrange_cards()
        for (let card_i in this.cards){
            this.cards[card_i].update()
        }
        this.cards= this.cards.filter(item => !(this.hand_delete.includes(item)))
        this.hand_delete=[]
        this.mana_bar.update()
        //this.sort_cards()
    }

    draw(){
        const cards_arr=this.sort_cards()
        this.mana_bar.draw(this.canvas,this.ctx,this.camera)
        for (let card_i in cards_arr){
            cards_arr[card_i].draw(this.camera,this.ctx,this.canvas)
            
        }
    }

    arrange_cards(){
        if (this.cards_mode=="ignore"){
            
            const angle_between=3*math.pi/180
            const radius=100

            
            const start_angle=-angle_between*(this.cards.length-1)/2
            for (let card_i in this.cards){
                const position=math.multiply(rotateZ(start_angle+card_i*angle_between),math.matrix([[0],[-radius],[0]]));

                //position=math.multiply(rotateZ(-angle_between),position);
                
                const position_arr=[position.get([0,0])+20,position.get([1,0])+radius+20,position.get([2,0])]
                this.cards[card_i].start_moving("move_to",[position_arr])
                this.cards[card_i].angle_z=start_angle+card_i*angle_between
                //this.cards[card_i].change_size(1)

                
            }
            
        }
        else{
            const angle_between=1*math.pi/180
            const radius=500

            
            const start_angle=-angle_between*(this.cards.length-1)/2
            for (let card_i in this.cards){
                const position=math.multiply(rotateZ(start_angle+card_i*angle_between),math.matrix([[0],[-radius],[0]]));

                //position=math.multiply(rotateZ(-angle_between),position);
                
                const position_arr=[position.get([0,0]),position.get([1,0])+radius+15,position.get([2,0])]
                this.cards[card_i].start_moving("move_to",[position_arr])
                this.cards[card_i].angle_z=start_angle+card_i*angle_between
            }
        }
    }
    sort_cards(){
        return this.cards.slice().sort(function(a, b) {
            return a.z_index - b.z_index;
          });
    }

    // draw_player(camera,ctx,){

    // }
}




