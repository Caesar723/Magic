class Show_2D{

    constructor(canvas,ctx){
        this.camera=new Camera([0,0,-50])
        this.card_frame=new Card_frame()
        this.canvas=canvas;
        this.ctx=ctx;

    }

    update(){
        this.update_showed_card()
    }
    draw(){
        this.draw_showed_card()
    }
    update_showed_card(){
        if (!(this.showed_card===undefined)){
            this.showed_card.update()
        }
    }
    show_a_card(card){
        this.showed_card=card.get_copy()
        this.showed_card.position=[-50,0,0]
        this.showed_card.moving_cache.push(["move_to",[[-20,0,0]]])
        this.showed_card.update()

    }


    draw_showed_card(){
        if (!(this.showed_card===undefined)){
            this.showed_card.draw(this.camera,this.ctx,this.canvas)
        }
    }


    unshow_a_card(){
        this.showed_card=undefined
    }
}