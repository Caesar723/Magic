
class Selection_Page{
    constructor(canvas,ctx,table,self_player,oppo_player){
        this.camera=new Camera([0,0,-50])
        this.card_frame=new Card_frame()
        this.canvas=canvas;
        this.ctx=ctx;
        this.table=table;
        this.self_player=self_player;
        this.oppo_player=oppo_player;

        this.in_selection=false


        this.selection_list=[]
        // for (let i=0 ;i<10;i++){
        //     const can=this.card_frame.generate_card("blue","Caesar","creature","Common","shausoaishaisuhai","cards/creature/Angelic Protector/image.jpg")
        //     const card=new Creature_Hand(4,5.62,[0,0,60],1.6,can,"10UU",20,20,20,20,"Caesar",1122334455)
        //     this.selection_list.push(card)
        // }
        
        
        this.selection_mode=''
        this.initinal_matrix(this.selection_list.length)

        const self_battlefield=table.get_self_battlefield.bind(table)
        const opponent_battlefield=table.get_opponent_battlefield.bind(table)
        const self_landfield=table.get_self_landfield.bind(table)
        const opponent_landfield=table.get_opponent_landfield.bind(table)

        this.selection_dict={
            'all_roles':[self_battlefield,opponent_battlefield,self_player,oppo_player],
            'opponent_roles':[oppo_player,opponent_battlefield],
            'your_roles':[self_player,self_battlefield],
            'all_creatures':[self_battlefield,opponent_battlefield],
            'opponent_creatures':[opponent_battlefield],
            'your_creatures':[self_battlefield],
            'all_lands':[self_landfield,opponent_landfield],
            'opponent_lands':[opponent_landfield],
            'your_lands':[self_landfield]
        }
        this.name_field=new Map();
        this.name_field.set(self_battlefield, "self_battlefield");
        this.name_field.set(opponent_battlefield, "opponent_battlefield");
        this.name_field.set(self_landfield, "self_landfield");
        this.name_field.set(opponent_landfield, "opponent_landfield");
    }

    set_selection_page(cards){
        console.log(cards)
        let copy_cards=[]
        for (let card of cards){
            const hand_card=Animation.check_hand(card,false,this.self_player)
            copy_cards.push(hand_card.get_copy())
        }
        this.selection_list=copy_cards
        this.initinal_matrix(cards.length)
    }

    start_selection(mode,cards){
        if (mode=="cards"){
            this.selection_mode=mode
            this.in_selection=true
            this.set_selection_page(cards)
        }
        else if (mode in this.selection_dict){
            this.selection_mode=mode
            this.in_selection=true
            for (let element of this.selection_dict[mode]){
                if (element instanceof Player){
                    element.start_selection()
                }
                else{
                    for (let card of element()){

                        if ((!get_dict(card.flag_dict,'Hexproof')) || card.player===this.self_player.type_name){

                            card.select_flag=true
                        }
                    }
                    console.log(element())
                }
            }
        }
    }
    end_selection(){
        if (this.selection_mode=="cards"){
            this.selection_mode=''
            this.in_selection=false
            this.selection_list=[]
            
        }
        else if (this.selection_mode in this.selection_dict){
            
            for (let element of this.selection_dict[this.selection_mode]){
                if (element instanceof Player){
                    element.end_selection()
                }
                else{
                    for (let card of element()){
                        card.select_flag=false
                    }
                }
            }
            this.selection_mode=''
            this.in_selection=false
        }
    }

    check_card_in_list(card){// 返回true false
        
        if (!(card instanceof Player) && get_dict(card.flag_dict,'Hexproof') && card.player===this.oppo_player.type_name){
            return false
        }
        if (this.selection_mode=="cards"){
            for(let element of this.selection_list){
                if (element===card){
                    return true
                }
            }
            
        }
        else if (this.selection_mode in this.selection_dict){
            for (let element of this.selection_dict[this.selection_mode]){
                if (element instanceof Player ){
                    if (element===card){
                        return true
                    }

                }
                else {
                    const element_list=element()
                    for(let each of element_list){
                        if (each===card){
                            return true
                        }
                    }
                }
            }

        }
        return false
    }

    check_mouse_in_selection(mouse_pos){//返回card或者是undefine
        if (this.selection_mode=="cards"){
            for(let card of this.sort_cards_check()){
                if (card.check_inside(mouse_pos,...card.position_in_screen)){
                    return card
                }
            }
            
        }
        else if (this.selection_mode in this.selection_dict){
            for (let element of this.selection_dict[this.selection_mode]){
                if (element instanceof Player ){
                    if (element.check_inside(mouse_pos,...element.player_life_ring.position_in_screen)){
                        return element
                    }

                }
                else {
                    const element_list=element()
                    for(let card of element_list){
                        if (card.check_inside(mouse_pos,...card.position_in_screen)){
                            return card
                        }
                    }
                }
            }

        }
        return undefined
    }

    get_object_parameter(obj){
        console.log(obj)
        if (this.selection_mode=="cards"){
            //console.log(this.sort_cards_check())
            for(let i in this.selection_list){
                if (this.selection_list[i]===obj){
                    return [this.self_player.name,"cards",i]
                }

            }
        }
        else if (this.selection_mode in this.selection_dict){
            for (let element of this.selection_dict[this.selection_mode]){
                if (element instanceof Opponent ){
                    if (obj===element){
                        return [this.self_player.name,"field","oppo"]
                    }
                    

                }
                else if (element instanceof Self){
                    if (obj===element){
                        return [this.self_player.name,"field","self"]
                    }

                }
                else {
                    const element_list=element()
                    for(let i in element_list){
                        if (element_list[i]===obj){
                            const name=this.name_field.get(element)
                            return [this.self_player.name,"field",name,i]
                        }
                    }
                }
            }
        }
    }
    initinal_matrix(length){//一个点绕着y轴旋转
        let initinal_point=math.matrix([[0],[0],[-20]])
        const arr_x=[];
        const arr_y=[];
        const arr_z=[];
        if (length<10){
            var len=10;
        }
        else{
            var len=length;
        }
        for (let i=0 ;i<length;i++){
            const angle=(2*math.pi/len)*(-i)
            var new_point=math.multiply(rotateY(angle),initinal_point);
            arr_x.push(new_point.get([0,0]));
            arr_y.push(new_point.get([1,0]));
            arr_z.push(new_point.get([2,0]));
            //console.log(i*(360/length))
        }
        this.points=math.matrix([arr_x,arr_y,arr_z,])
        //console.log(this.points)
    }

    rotate_cards(deltaX){
        if (this.selection_mode=="cards" && this.in_selection){
            
            
            this.points=math.multiply(rotateY(deltaX/40),this.points);
            
        }
    }
    set_position(){
        
        for (let col=0;col<this.selection_list.length;col++){
            
            this.selection_list[col].position=[
                this.points.get([0,col]),
                this.points.get([1,col]),
                this.points.get([2,col])
            ]
        }
    }

    update(){
        if (this.selection_mode=="cards" && this.in_selection){
            for (let card of this.selection_list){
                card.update()
            }
            this.set_position()
            //console.log(this.points)
        }
    }
    draw(){
        if (this.selection_mode=="cards" && this.in_selection){
            //console.log(this.sort_cards(),this.selection_list)
            for (let card of this.sort_cards()){
                card.draw(this.camera,this.ctx,this.canvas)
            }
        }
    }
    sort_cards(){
        return this.selection_list.slice().sort(function(a, b) {
            return -a.position[2] + b.position[2];
          });
    }
    sort_cards_check(){
        return this.selection_list.slice().sort(function(a, b) {
            return a.position[2] - b.position[2];
          });
    }
}






