class Player{
    constructor(name,canvas,ctx){
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
}

class Opponent extends Player{

}

class Self extends Player{
    constructor(name,canvas,ctx){
        super(name,canvas,ctx);

        const canvas_dynamic=this.card_frame.generate_card("blue","Caesar","creature","Common","shausoaishaisuhai","cards/creature/Angelic Protector/image.jpg")
        const card=new Creature_Hand(4,5.62,[0,0,0],1.5,canvas_dynamic,"3U",20,20,"Caesar",1122334455,this)
        

        this.cards=[card];
        this.hand_delete=[]

        this.cards_mode="ignore"//两个模式，第一个是ignore，卡牌缩小，放到右侧，第二个是focus，卡牌放大
    }
    change_to_ignore(){
        if (this.cards_mode=="focus"){
            this.cards_mode="ignore"
            console.log(123)
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
                
                const position_arr=[position.get([0,0]),position.get([1,0])+radius+10,position.get([2,0])]
                this.cards[card_i].start_moving("enlarge",[position_arr])
                //this.cards[card_i].moving_cache.push(["enlarge",[position_arr]])
                this.cards[card_i].angle_z=start_angle+card_i*angle_between
            }
        }
        
    }
    update(){

        this.arrange_cards()
        for (let card_i in this.cards){
            this.cards[card_i].update()
        }
        this.cards= this.cards.filter(item => !(this.hand_delete.includes(item)))
        this.hand_delete=[]
    }

    draw(){
        for (let card_i in this.cards){
            this.cards[card_i].draw(this.camera,this.ctx,this.canvas)
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
                
                const position_arr=[position.get([0,0]),position.get([1,0])+radius+10,position.get([2,0])]
                this.cards[card_i].start_moving("move_to",[position_arr])
                this.cards[card_i].angle_z=start_angle+card_i*angle_between
            }
        }
    }
}