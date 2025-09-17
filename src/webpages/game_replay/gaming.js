class Game_Client{
    constructor(){
        this.main_canvas=document.getElementById("myCanvas");
        
        this.socket_main=null;
        this.socket_select =null;

        
        this.table=new Table(this)
        this.canvas_table=this.table.canvas
        this.ctx_table=this.table.ctx
        //this.main_ctx=this.main_canvas.getContext("2d");
        this.table.camera.update()
       
        this.win_lose=new Winning_And_Losing(this.canvas_table,this.ctx_table)
        let players=window.dataFromBackend
        
        this.self_player=new Self(players["self"],this.canvas_table,this.ctx_table)
        this.oppo_player=new Opponent(players["opponent"],this.canvas_table,this.ctx_table)
        this.music=new Music(this.self_player,this.oppo_player)

        console.log(this.self_player,this.oppo_player)
        this.table.set_player(this.self_player,this.oppo_player)
        //this.initinal_players()
        

        this.card_frame=new Card_frame()
        this.action_bar=new Action_Bar()
        this.show_2d=new Show_2D(this.canvas_table,this.ctx_table)
        this.buttons=new Buttons(this)

        this.selectionPage=new Selection_Page(this.canvas_table,this.ctx_table,this.table,this.self_player,this.oppo_player)
        
        //////////////////////////////
        //const canvas=this.card_frame.generate_card("blue","Caesar","creature","Common","shausoaishaisuhai","cards/creature/Angelic Protector/image.jpg")
        //const card=new Creature_Hand(4,5.62,[0,0,60],1.6,canvas,"3U",20,20,20,20,"Caesar",1122334455)
        // this.action_bar.actions.push(new Activate_Ability(card.get_copy(),this.self_player))
        // this.action_bar.actions.push(new Die(card.get_copy(),this.self_player))
        // this.action_bar.actions.push(new Summon(card.get_copy(),this.self_player))
        // this.action_bar.actions.push(new Turn(card.get_copy(),this.self_player))
        // this.action_bar.actions.push(new Change_Mana(card.get_copy(),this.self_player))
        ////////////////////////////////////////


        console.log(this.ctx_table)

        this.set_lestener()

        this.mouse_hold=false//判断mouse是否抓住牌
        this.card_hold=[undefined,false,false]//card click bool,move bool

        //this.init()
        

        this.your_turn=true;//判断是不是你的回合
        this.message_processor=new Message_Processor(this)
        this.game_player=new Game_Player(this.message_processor,this)

        
        this.resolveSelectInput= '';

        this.grayscale=0;
        this.blur_value=0;
    }
    // async initinal_players(){
    //     console.log(await this.get_players_name())
        
       
    // }
    // async get_players_name(){
    //     const response = await fetch('/players', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json'
    //         },
            
    //     });
    //     const responseData =await response.json()
    //     return responseData
    // }
    async init() {
        
    }

   

    
    get_domain(name){
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.hostname;
        const port = window.location.port ? `:${window.location.port}` : '';
        const socketUrl = `${protocol}//${host}${port}/${name}`;
        return socketUrl
    }
    async get_socket_main(){
        this.socket_main= new WebSocket(this.get_domain("entering_game"));
        this.receive_message_main_listener()
        while (this.socket_main.readyState != WebSocket.OPEN){
            await this.sleep(200)
        }
        //return socket
    }
    async get_socket_select(){
        this.socket_select = new WebSocket(this.get_domain("select_object"));
        this.receive_message_select_listener()
        while (this.socket_select.readyState != WebSocket.OPEN){
            await this.sleep(200)
        }
        //return socket
    }
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    

    
    massage_process_main(message){

    }

    
    massage_process_select(message){

    }

    

    update(){
        this.game_player.update()
        this.action_bar.update()
        this.table.update()
        
        this.oppo_player.update()
        this.self_player.update()
        
        this.show_2d.update()
        this.buttons.update()
        this.selectionPage.update()
        

        this.blur_changing()
    }
    draw(){
        //this.ctx_table.filter = 'grayscale(100%)';
        //console.time('table');
        this.table.draw()
        //console.timeEnd('table');

        //console.time('oppo_player');
        this.oppo_player.draw()
        //console.timeEnd('oppo_player');

        //console.time('self_player');
        this.self_player.draw()
        //console.timeEnd('self_player');

        this.ctx_table.filter = 'none';
        if (this.action_bar.mode=="show"){
            this.blur_effect(this.grayscale,this.blur_value)
        }
        this.action_bar.draw(this.canvas_table,this.ctx_table,this.self_player.camera)
        this.show_2d.draw()
        this.buttons.draw(this.canvas_table,this.ctx_table)
        if ((this.selectionPage.in_selection && this.selectionPage.selection_mode=="cards")||(this.win_lose.finish) ){
            this.blur_effect(this.grayscale,this.blur_value)
        }
        this.selectionPage.draw()
        this.win_lose.draw()

        //this.main_ctx.drawImage(this.canvas_table, this.main_canvas.width,this.main_canvas.height)




    }
    blur_changing(){
        const value_change_grayscale=5
        const value_change_blur=0.5
        var max_blur=0;
        var max_grayscale=0;

        if (this.action_bar.mode=="show"){
            max_blur=10
            max_grayscale=50
            //this.blur_effect(50,10)
        }
        if (this.selectionPage.in_selection && this.selectionPage.selection_mode=="cards" ){
            max_blur=10
            max_grayscale=100
            //this.blur_effect(100,10)
        }
        if (this.win_lose.finish ){
            max_blur=10
            max_grayscale=100
        }

        if (max_blur==0 && max_grayscale==0){
            this.grayscale-=value_change_grayscale
            this.blur_value-=value_change_blur

            if (this.grayscale<max_grayscale){
                this.grayscale=max_grayscale
            }
            if (this.blur_value<max_blur){
                this.blur_value=max_blur
            }

        }
        else{
            this.grayscale+=value_change_grayscale
            this.blur_value+=value_change_blur

            if (this.grayscale>max_grayscale){
                this.grayscale=max_grayscale
            }
            if (this.blur_value>max_blur){
                this.blur_value=max_blur
            }
        }
    }
    set_lestener(){
        this.main_canvas.addEventListener('wheel', (event)=> {
            //console.log(event.deltaY);
            //this.table.camera.angle_x=event.deltaX/40+this.table.camera.angle_x
            //this.table.camera.angle_y=event.deltaY/40+this.table.camera.angle_y
            if (this.selectionPage.in_selection==false){
                this.table.camera.add_rotate_prescent(event.deltaY)
                this.table.camera.update()
            }
            

            this.selectionPage.rotate_cards(event.deltaX)
           
            event.preventDefault();
        });
        this.main_canvas.addEventListener('mousemove', (event) => {
            
            if (this.card_hold[2]){
                this.show_2d.delete_mouse_card()
                const mouse_pos=this.get_mouse_pos(event,this.main_canvas)
                //console.log(2)
                if (this.card_hold[0] instanceof Card_Battle){
                    //console.log(this.card_hold[0].position[2],this.card_hold[0].position_in_screen_z)
                    //const next_pos=this.table.camera.similar_tri_reverse_2(...mouse_pos,this.card_hold[0].position[1],this.card_hold[0].position_in_screen_z);
                    this.card_hold[0].moving_by_mouse(mouse_pos,this.table.camera)
                    
                }
                else if(this.card_hold[0] instanceof Card_Hand){
                    this.card_hold[0].moving_by_mouse(mouse_pos,this.self_player.camera)
                    
                }
            }
            else if(this.card_hold[0]===undefined){
                const mouse_pos=this.get_mouse_pos(event,this.main_canvas)
                const card=this.find_cards_by_mouse(mouse_pos)
                const timer=this.find_timers_by_mouse(mouse_pos)
                const action=this.action_bar.check_mouse(mouse_pos)
                const button=this.find_button_by_mouse(mouse_pos)

                const object=this.selectionPage.check_mouse_in_selection(mouse_pos)



                if ( ((!(card===undefined)||!(timer===undefined )||!(button===undefined ))&&!this.selectionPage.in_selection) || (this.selectionPage.in_selection&&!(object===undefined)) ){
                    this.main_canvas.style.cursor = 'pointer';
                }
                else{
                    this.main_canvas.style.cursor = 'default';
                }
                //console.log(11)
                if (card instanceof Card_Hand){
                    
                    for (let i in this.self_player.cards){
                        if (this.self_player.cards[i]!=card){
                            
                            this.self_player.cards[i].start_moving("change_size_animation",[this.self_player.get_small_size()])
                            
                            this.self_player.cards[i].z_index=1;
                            
                        }
                        
                    }
                    card.start_moving("change_size_animation",[this.self_player.get_enlarge_size()])
                    card.z_index=2;
                    
                    //this.canvas_table.style.cursor = 'pointer';             
                    //card.change_size_cache=this.self_player.get_enlarge_size()
                }
                else{
                    for (let i in this.self_player.cards){
                        if (this.self_player.cards[i]!=card){
                            //console.log(this.self_player.get_small_size())
                            this.self_player.cards[i].start_moving("change_size_animation",[this.self_player.get_small_size()])
                            //console.log(this.self_player.cards[i].size)
                            this.self_player.cards[i].z_index=1;
                            
                        }
                        
                    }

                    
                    if (card instanceof Card_Battle){
                        console.log(card.card,card.position)
                        this.show_2d.set_mouse_card(card.card,card.position)
                    }
                    else{
                        this.show_2d.delete_mouse_card()
                    }
                    

                    //this.canvas_table.style.cursor = 'default';
                    
                }

                
                if (timer===undefined){
                    this.table.timmer_turn.mode="time"
                    this.table.timmer_bullet.mode="time"
                    
                }
                else{
                    timer.mode="end"
                }
                
                if (action){
                    this.action_bar.card_mode="show"//show hide
                    this.action_bar.action_showed=action
                }
                else{
                    this.action_bar.card_mode="hide"//show hide
                    this.action_bar.action_showed=undefined
                }
                

            }
        });
        this.main_canvas.addEventListener('mouseup', (event) => {
            if (!(this.card_hold[0]===undefined)){
                
                
                if (this.card_hold[0] instanceof Card_Battle){
                    
                    
                    this.card_hold[0].angle_x=math.pi/2;;
                    this.card_hold[0].angle_y=0;
                    //this.card_hold[0].angle_z=0;
                    

                    
                }
                else if(this.card_hold[0] instanceof Card_Hand){
                    this.card_hold[0].angle_x=0;
                    this.card_hold[0].angle_y=0;
                    this.card_hold[0].angle_z=0;
                    if (performance.now()-this.startTime<0.15*1000){
                        this.self_player.change_to_focus()
                    }
                    else{
                        //const mouse_pos=this.get_mouse_pos(event,this.main_canvas)
                        //this.hand_move_activate(this.card_hold[0],mouse_pos)
                    }
                    // if (this.card_hold[1]){
                        
                    // }
                }
                this.card_hold[0].card_hold=[false,false]
                this.card_hold=[undefined,false,false]
            }
            else{
                const mouse_pos=this.get_mouse_pos(event,this.main_canvas)
                const timer=this.find_timers_by_mouse(mouse_pos)
                if (performance.now()-this.startTime<0.15*1000 && (timer===undefined) ){
                    this.self_player.change_to_ignore()
                        
                    //console.log("click")
                }
            }
        });
        
        this.main_canvas.addEventListener('mousedown', (event) => { 
            const mouse_pos=this.get_mouse_pos(event,this.main_canvas)
            const card=this.find_cards_by_mouse(mouse_pos)
            
            const object=this.selectionPage.check_mouse_in_selection(mouse_pos)
            if (object===undefined && this.selectionPage.in_selection){
                //this.resolveSelectInput("cancel_client")
            }
            else if (! (object===undefined)){
                //this.end_selection(object)
            }
            else if (! (card===undefined)){
                //console.log(card)
                const click_bool=this.judge_click(card)
                const move_bool=this.judge_move(card)
                this.card_hold=[card,click_bool,move_bool]
                card.card_hold=[click_bool,move_bool]
                
            }
            this.startTime = performance.now();

            
            
            
            
        });

        
        

       
        
    }
    find_cards_by_mouse(mouse_pos){//会检查你点到是哪一张牌
        const cards_hand_self=this.self_player.cards//先检查hand的，从右往左
        const cards_hand_oppo=this.oppo_player.cards//
        const cards_battle_self=this.table.self_battlefield//再检查battle的
        const cards_battle_oppo=this.table.opponent_battlefield
        const cards_land_self=this.table.self_landfield//再检查land的
        const cards_land_oppo=this.table.opponent_landfield

        const cards=[cards_hand_self,cards_hand_oppo,cards_battle_self,cards_battle_oppo,cards_land_self,cards_land_oppo]
        for (let cards_i in cards){
            const card=this.check_cards_list(mouse_pos,cards[cards_i])
            
            if (! (card===undefined)){
                return card
            }
        }

        return undefined
    }
    check_cards_list(mouse_pos,arr){
        for (let i in arr){
            const index=arr.length-i-1
            //console.log(arr[index],arr[index].position_in_screen,arr[index].check_inside(mouse_pos,...arr[index].position_in_screen))
            if (arr[index].check_inside(mouse_pos,...arr[index].position_in_screen)){
                return arr[index]
            }
        }
        return undefined
    }
    find_timers_by_mouse(mouse_pos){
        if (this.table.timmer_turn.check_inside(mouse_pos,...this.table.timmer_turn.position_in_screen)){
            //console.log(12345)
            return this.table.timmer_turn
        }
        else if(this.table.timmer_bullet.check_inside(mouse_pos,...this.table.timmer_bullet.position_in_screen)){
            //console.log(345)
            return this.table.timmer_bullet
        }
        return undefined
    }
    find_button_by_mouse(mouse_pos){
        
        return this.buttons.find_button_by_mouse(mouse_pos)
    }
    get_mouse_pos(event,canvas){
        var rect = canvas.getBoundingClientRect();
        // 计算鼠标相对于canvas的位置
        var mouseX = (event.clientX - rect.left)*canvas.width/rect.width;
        var mouseY = (event.clientY - rect.top)*canvas.height/rect.height;
        return [mouseX,mouseY]
    }

    judge_move(card){
        return true
    }
    judge_click(card){
        return true
    }



    mouse_process(){

    }

    card_hand_mouse_process(){

    }

    timmer_mouse_process(){

    }

    action_mouse_process(){

    }

    check_battle(card,player){//如果card是hand，检查有没有battle，没有就建一个
        if (card instanceof Card_Battle){
            return card
        }
        else if(card instanceof Card_Hand){
            if (card.battle===undefined){
                new Land_Battle(6,5,[-25,-20,0],0.3,card,player.type_name,this.table)
            }
            return card.battle
        }
    }
    check_hand(card,battle_bool,player){//如果card是battle，变成hand，如果battle_bool是true，检查有没有battle，没有就建一个
        if (battle_bool){
            this.check_battle(card,player)
        }
        if (card instanceof Card_Battle){
            return card.card
        }
        else if(card instanceof Card_Hand){
            return card
        }
    }
    battle_click_activate(card){
        if (card instanceof Land_Battle){
            for (let card_self_land_i in this.table.self_landfield){
                if(this.table.self_landfield[card_self_land_i]===card){
                    const values = [this.self_player.name,'activate_ability',`land_area;${card_self_land_i}`];
                    this.socket_main.send(values.join('|'));
                    return true
                }
            }
        }
        return false   
    }
    battle_move_activate(card){
        if (card instanceof Creature_Battle && ((card.position_in_screen[1][1]+card.position_in_screen[2][1])/2<this.canvas_table.height/2.5)){
            if (this.table.player_self.my_turn){
                for (let card_self_battle_i in this.table.self_battlefield){
                    if(this.table.self_battlefield[card_self_battle_i]===card){
                        const values = [this.self_player.name,'select_attacker',card_self_battle_i];
                        this.socket_main.send(values.join('|'));
                        return true
                    }
                }
            }
            else{
                for (let card_self_battle_i in this.table.self_battlefield){
                    if(this.table.self_battlefield[card_self_battle_i]===card){
                        const values = [this.self_player.name,'select_defender',card_self_battle_i];
                        this.socket_main.send(values.join('|'));
                        return true
                    }
                }
            }
            
        }
        return false
    }
    hand_move_activate(card,mouse_pos){
        //(card.position_in_screen[1][1]+card.position_in_screen[2][1])/2
        if (mouse_pos[1]<this.canvas_table.height/2){
            for (let card_self_hand_i in this.self_player.cards){
                if(this.self_player.cards[card_self_hand_i]===card){
                    const values = [this.self_player.name,'play_card',card_self_hand_i];
                    this.socket_main.send(values.join('|'));
                    return true
                }
            }
        }
        return false
    }
    end_time(timer){
        if (timer.name=='turn'){
            const values = [this.self_player.name,'end_step',''];
            this.socket_main.send(values.join('|'));
            return true
        }
        else if (timer.name=='bullet'){
            const values = [this.self_player.name,'end_bullet',''];
            this.socket_main.send(values.join('|'));
            return true
        }
    }
    find_position(card){//return position name and index
        for (let card_self_hand_i in this.self_player.cards){
            if(this.self_player.cards[card_self_hand_i]===card){
                return ('hand',card_self_hand_i)
            }
        }
        for (let card_self_battle_i in this.table.self_battlefield){
            if(this.table.self_battlefield[card_self_battle_i]===card){
                return ('battlefield',card_self_battle_i)
            }
        }
        for (let card_self_land_i in this.table.self_landfield){
            if(this.table.self_landfield[card_self_land_i]===card){
                return ('land_area',card_self_land_i)
            }
        }
        for (let card_oppo_hand_i in this.oppo_player.cards){
            if(this.self_player.cards[card_oppo_hand_i]===card){
                return ('hand',card_oppo_hand_i)
            }
        }
        
        for (let card_oppo_battle_i in this.table.opponent_battlefield){
            if(this.table.opponent_battlefield[card_oppo_battle_i]===card){
                return ('battlefield',card_oppo_battle_i)
            }
        }
        
        for (let card_oppo_land_i in this.table.opponent_landfield){
            if(this.table.opponent_landfield[card_oppo_land_i]===card){
                return ('land_area',card_oppo_land_i)
            }
        }
        return false
        
    }

    blur_effect(grayscale,blur_value){
        this.ctx_table.filter =  `blur(${blur_value}px) grayscale(${grayscale}%)`;
        this.ctx_table.drawImage(this.canvas_table, 0, 0, this.canvas_table.width, this.canvas_table.height);
        this.ctx_table.filter =  "none";
    }

    //////////////////////////////////////////////////
    end_selection(card){
        if (this.selectionPage.check_card_in_list(card)){
            
            this.resolveSelectInput(card)
        }
        
    }
    get_selected_input(){
        return new Promise((resolve) => {
            this.resolveSelectInput = resolve;
        });
    }
    // select_object(){

    // }

}

class Winning_And_Losing{
    constructor(canvas,ctx){
        this.canvas=canvas;
        this.ctx=ctx;
        this.finish=false
        this.win = new Image();
        this.win.src="webpages/image_source/game/win.png";

        this.lose = new Image();
        this.lose.src="webpages/image_source/game/lose.png";
        this.show_pic=new Image();

        // this.finish=true
        // this.show_pic=this.lose
    }
    set_picture(isWin){
        if (isWin){
            this.show_pic=this.win
        }
        else{
            this.show_pic=this.lose
        }
        this.finish=true
        
    }
    draw(){
        if (this.finish){
            const x = (this.canvas.width - this.show_pic.width) / 2;
            const y = (this.canvas.height - this.show_pic.height) / 2;
            this.ctx.drawImage(this.show_pic, x, y);
        }
    }
}

// (async () => {
//     const client = new GameClient();
//     await client.init();
//     // 现在 client.socket 应该已经准备好了
// })();



