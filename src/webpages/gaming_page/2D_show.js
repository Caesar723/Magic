class Show_2D{

    constructor(canvas,ctx){
        this.camera=new Camera([0,0,-50])
        this.card_frame=new Card_frame()
        this.canvas=canvas;
        this.ctx=ctx;

    }

    update(){
        this.update_showed_card()
        this.update_mouse_card()
    }
    draw(){
        this.draw_showed_card()
        this.draw_mouse_card()
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


    set_mouse_card(card,position){
        //if (!(this.mouse_card===undefined)){
        this.mouse_card=card.get_copy()
        const distance=3*(card.size)+10

        if (position[0]>0){
            this.mouse_card.position=[position[0]-distance,0,0]///
        } 
        else{
            this.mouse_card.position=[position[0]+distance,0,0]///
        }  
        
        console.log()
        //}
        

    }
    delete_mouse_card(){
        this.mouse_card=undefined
    }
    update_mouse_card(){
        if (!(this.mouse_card===undefined)){
            this.mouse_card.update()
        }
    }
    draw_mouse_card(){
        if (!(this.mouse_card===undefined)){
            this.mouse_card.draw(this.camera,this.ctx,this.canvas)
            for (let buff_index in this.mouse_card.buff_list){
                console.log( [this.mouse_card.position_in_screen[1][1],this.mouse_card.position_in_screen[3][1]+buff_index*50])
                const position=[
                    (this.mouse_card.position_in_screen[2][0]+this.mouse_card.position_in_screen[1][0])/2-100,
                    this.mouse_card.position_in_screen[1][1]+buff_index*50
                ]
                this.mouse_card.buff_list[buff_index].draw(position,this.ctx,this.canvas)
            }
        }
    }
}