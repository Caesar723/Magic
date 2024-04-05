class Game_Client{
    constructor(){
        this.socket_main=null;
        this.socket_select =null;

        this.table=new Table()
        this.canvas_table=this.table.canvas
        this.ctx_table=this.table.ctx

        this.self_player=new Self("CC",this.canvas_table,this.ctx_table)
        this.oppo_player=new Opponent("DD",this.canvas_table,this.ctx_table)
        this.table.set_player(this.self_player,this.oppo_player)
        this.card_frame=new Card_frame()


        this.action_bar=new Action_Bar()
        //////////////////////////////
        const canvas=this.card_frame.generate_card("blue","Caesar","creature","Common","shausoaishaisuhai","cards/creature/Angelic Protector/image.jpg")
        const card=new Creature_Hand(4,5.62,[0,0,60],1.6,canvas,"3U",20,20,"Caesar",1122334455)
        this.action_bar.actions.push(new Activate_Ability(card.get_copy(),this.self_player))
        this.action_bar.actions.push(new Die(card.get_copy(),this.self_player))
        this.action_bar.actions.push(new Summon(card.get_copy(),this.self_player))
        this.action_bar.actions.push(new Turn(card.get_copy(),this.self_player))
        this.action_bar.actions.push(new Change_Mana(card.get_copy(),this.self_player))
        ////////////////////////////////////////


        console.log(this.ctx_table)

        this.set_lestener()

        this.mouse_hold=false//判断mouse是否抓住牌
        this.card_hold=[undefined,false,false]//card click bool,move bool

        this.init()



    }
    async init() {
        this.socket_main = await this.get_socket("entering_game");
        this.socket_select = await this.get_socket("select_object");
    }
    async get_socket(name){
        var socket = new WebSocket("ws://127.0.0.1:8000/"+name);
        while (socket.readyState != WebSocket.OPEN){
            await this.sleep(200)
        }
        return socket
    }
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    

    receive_message_main_listener(){

        this.socket_main.addEventListener('message', (event)=> {
            console.log('收到消息：', event.data);
            // 在这里处理消息
            // 你可以根据消息的内容执行不同的操作，比如更新UI、存储数据等
          });
        this.socket_main.addEventListener('close', () => {

        });
        this.socket_main.addEventListener('error', (event) => {
            
        });
    }
    massage_process_main(message){

    }

    receive_message_select_listener(){
        // while (this.socket_select.readyState === WebSocket.OPEN){

        // }
        this.socket_select.addEventListener('message', (event)=> {
            console.log('收到消息：', event.data);
            // 在这里处理消息
            // 你可以根据消息的内容执行不同的操作，比如更新UI、存储数据等
          });
        this.socket_select.addEventListener('close', () => {

        });
        this.socket_select.addEventListener('error', (event) => {
            
        });
    }
    massage_process_select(message){

    }

    

    update(){
        this.table.update()
        this.oppo_player.update()
        this.self_player.update()
        this.action_bar.update()
    }
    draw(){
        //this.ctx_table.filter = 'grayscale(100%)';
        this.table.draw()
        this.oppo_player.draw()
        this.self_player.draw()
        this.ctx_table.filter = 'none';
        this.action_bar.draw(this.canvas_table,this.ctx_table,this.self_player.camera)


    }
    set_lestener(){
        

        
        this.canvas_table.focus()
        this.canvas_table.addEventListener('keydown', (event) => {
            console.log("A key pressed");
            if (event.key === "w" || event.key === "W") {
                // 执行W键按下时的操作
                this.table.camera.position[2]=this.table.camera.position[2]+1
            } else if (event.key === "a" || event.key === "A") {
                // 执行A键按下时的操作
                this.table.camera.position[0]=this.table.camera.position[0]-1
            } else if (event.key === "s" || event.key === "S") {
                // 执行S键按下时的操作
                this.table.camera.position[2]=this.table.camera.position[2]-1
            } else if (event.key === "d" || event.key === "D") {
                // 执行D键按下时的操作
                this.table.camera.position[0]=this.table.camera.position[0]+1
            }
            else if (event.key ===' ') {
                // 执行D键按下时的操作
                this.table.camera.position[1]=this.table.camera.position[1]-1
            }
            else if (event.shiftKey) {
                // 执行D键按下时的操作
                this.table.camera.position[1]=this.table.camera.position[1]+1
            }
            else if (event.key === "i" || event.key === "I") {
                // 执行D键按下时的操作
                this.table.self_battlefield[0].start_moving("move_to",[[0,-20,-30]])
            }
            else if (event.key === "p" ) {
                // 执行D键按下时的操作
                console.log(this.table.self_battlefield[0].card.get_copy())
                const action=new Creature_Start_Attack(this.table.self_battlefield[0].card.get_copy(),this.self_player,this.oppo_player,[10,10],[2])
                action.set_animate()
                this.action_bar.actions.push(action)
                // this.table.self_battlefield[0].moving_cache.push(["attack_to",[[15,-20,-10],[10,10]]])
                // this.table.self_battlefield[0].moving_cache.push(["rotate_to_point",[[
                //     this.table.self_battlefield[0].accurate_position[0],
                //     this.table.self_battlefield[0].accurate_position[1],
                //     this.table.self_battlefield[0].accurate_position[2]+1,
                // ]]])
            }
            else if (event.key === "q") {
                // 执行D键按下时的操作
                console.log(this.table.self_battlefield[0].card.get_copy())
                const action=new Creature_Start_Attack(this.table.self_battlefield[0].card.get_copy(),this.self_player,this.table.opponent_battlefield[0],[10,10],[10,2])
                action.set_animate()
                this.action_bar.actions.push(action)
                // this.table.self_battlefield[0].moving_cache.push(["attack_to",[[15,-20,-10],[10,10]]])
                // this.table.self_battlefield[0].moving_cache.push(["rotate_to_point",[[
                //     this.table.self_battlefield[0].accurate_position[0],
                //     this.table.self_battlefield[0].accurate_position[1],
                //     this.table.self_battlefield[0].accurate_position[2]+1,
                // ]]])
            }
            else if (event.key === "o" || event.key === "O") {
                // 执行D键按下时的操作
                this.table.self_battlefield[0].moving_cache.push(["rotate_to_point",[[15,-20,-10]]])
            }
            else if (event.key === "u" || event.key === "U") {
                // 执行D键按下时的操作
                this.table.self_battlefield[0].moving_cache.push(["disappear",[[0,-20,-20]]])
            }
            else if (event.key === "y" || event.key === "Y") {
                // 执行D键按下时的操作
                this.table.opponent_battlefield[0].start_moving("disappear",[[0,-20,20]])
            }
            else if (event.key === "l" || event.key === "L"){
                const canvas=this.table.card_frame.generate_card("blue","Caesar","creature","Common","shausoaishaisuhai","cards/creature/Angelic Protector/image.jpg")
                const card=new Creature_Hand(4,5.62,[0,0,60],1.6,canvas,"3U",20,20,"Caesar",1122334455)
                const card_battle=new Creature_Battle(6,5,[-25,-25,0],0.3,card,"self",this.table)
                this.table.self_battlefield.push(card_battle)
            }
            else if (event.key === "k" || event.key === "K"){
                const canvas=this.table.card_frame.generate_card("blue","Caesar","creature","Common","shausoaishaisuhai","cards/creature/Angelic Protector/image.jpg")
                const card=new Creature_Hand(4,5.62,[0,0,60],1.6,canvas,"3U","Caesar",1122334455)
                const card_battle=new Creature_Battle(6,5,[-25,-20,0],0.3,card,"opponent",this.table)
                this.table.opponent_battlefield.push(card_battle)
            }
            else if (event.key === "m" || event.key === "M"){
                this.self_player.cards[0].moving_cache.push(["move_to",[[0,0,0]]])
            }
            else if (event.key === "n" || event.key === "N"){
                this.self_player.cards[0].moving_cache.push(["move_to",[[5,0,0]]])
            }
            else if (event.key === "b" || event.key === "B"){
                const canvas_dynamic=this.self_player.card_frame.generate_card("blue","Caesar","creature","Common","shausoaishaisuhai","cards/creature/Angelic Protector/image.jpg")
                const card=new Creature_Hand(4,5.62,[0,60,-20],1.5,canvas_dynamic,"3U",20,20,"Caesar",1122334455,this.self_player)
        
                this.self_player.cards.push(card)
            }
            else if (event.key === "v" || event.key === "V") {
                
                this.self_player.cards[0].moving_cache.push(["disappear",[[0,60,-20]]])
            }
            else if (event.key === "c" || event.key === "C") {
                const card=new Card_Hand_Oppo(4,5.62,[0,-60,-20],0.7,1122334455,this.oppo_player)
        
                this.oppo_player.cards.push(card)
            }

            else if (event.key === "x" || event.key === "X") {
                this.table.timmer_turn.animate_set(this.table.timmer_turn.time-5,this.table.timmer_turn.time)
        
                //this.oppo_player.cards.push(card)
            }
            else if (event.key === "z" || event.key === "Z") {
                this.table.timmer_turn.animate_set(this.table.timmer_turn.time+5,this.table.timmer_turn.time)
        
                //this.oppo_player.cards.push(card)
            }
            else if (event.key === "f" || event.key === "F") {
                //this.table.timmer_turn.animate_set(this.table.timmer_turn.time+5,this.table.timmer_turn.time)
                this.self_player.player_life_ring.animate_set(this.self_player.player_life_ring.life+1,this.self_player.player_life_ring.life)
                //this.oppo_player.cards.push(card)
            }
            else if (event.key === "g" || event.key === "G") {
                //this.table.timmer_turn.animate_set(this.table.timmer_turn.time+5,this.table.timmer_turn.time)
                this.self_player.player_life_ring.animate_set(this.self_player.player_life_ring.life-3,this.self_player.player_life_ring.life)
                //this.oppo_player.cards.push(card)
            }


            
        });
        this.canvas_table.addEventListener('mousedown', (event) => { 
            const mouse_pos=this.get_mouse_pos(event,this.canvas_table)
            const card=this.find_cards_by_mouse(mouse_pos)
            if (! (card===undefined)){
                //console.log(card)
                const click_bool=this.judge_click()
                const move_bool=this.judge_move()
                this.card_hold=[card,click_bool,move_bool]
                card.card_hold=[click_bool,move_bool]
                
            }
            this.startTime = performance.now();
            
            
            
        });
        this.canvas_table.addEventListener('mousemove', (event) => {
            
            if (this.card_hold[2]){
                const mouse_pos=this.get_mouse_pos(event,this.canvas_table)
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
                const mouse_pos=this.get_mouse_pos(event,this.canvas_table)
                const card=this.find_cards_by_mouse(mouse_pos)
                const timer=this.find_timers_by_mouse(mouse_pos)
                const action=this.action_bar.check_mouse(mouse_pos)



                if (!(card===undefined)||!(timer===undefined)){
                    this.canvas_table.style.cursor = 'pointer';
                }
                else{
                    this.canvas_table.style.cursor = 'default';
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
        this.canvas_table.addEventListener('mouseup', (event) => {
            if (!(this.card_hold[0]===undefined)){
                
                
                if (this.card_hold[0] instanceof Card_Battle){
                    this.card_hold[0].angle_x=math.pi/2;;
                    this.card_hold[0].angle_y=0;
                    this.card_hold[0].angle_z=0;
                    
                }
                else if(this.card_hold[0] instanceof Card_Hand){
                    this.card_hold[0].angle_x=0;
                    this.card_hold[0].angle_y=0;
                    this.card_hold[0].angle_z=0;
                    if (this.card_hold[1]){
                        if (performance.now()-this.startTime<0.15*1000){
                            //console.log("click")
                            
                            this.self_player.change_to_focus()
                            
                        }
                    }
                }
                this.card_hold[0].card_hold=[false,false]
                this.card_hold=[undefined,false,false]
            }
            else{
                if (performance.now()-this.startTime<0.15*1000){
                    this.self_player.change_to_ignore()
                        
                    //console.log("click")
                }
            }
            
            
        });
        this.canvas_table.addEventListener('mouseleave', (event) => {
            if (!(this.card_hold[0]===undefined)){
                
                if (this.card_hold[0] instanceof Card_Battle){
                    this.card_hold[0].angle_x=math.pi/2;;
                    this.card_hold[0].angle_y=0;
                    this.card_hold[0].angle_z=0;
                    
                }
                else if(this.card_hold[0] instanceof Card_Hand){
                    this.card_hold[0].angle_x=0;
                    this.card_hold[0].angle_y=0;
                    this.card_hold[0].angle_z=0;
                }
                this.card_hold[0].card_hold=[false,false]
                this.card_hold=[undefined,false,false]
            }
        });

        this.canvas_table.addEventListener('wheel', (event)=> {
            //console.log(event.deltaY);
            this.table.camera.angle_x=event.deltaX/40+this.table.camera.angle_x
            this.table.camera.angle_y=event.deltaY/40+this.table.camera.angle_y
            // this.table.camera.add_rotate_prescent(event.deltaY)
            // this.table.camera.update()
           
            event.preventDefault();
        });

        
        

       
        
    }
    find_cards_by_mouse(mouse_pos){//会检查你点到是哪一张牌
        const cards_hand_self=this.self_player.cards//先检查hand的，从右往左
        const cards_hand_oppo=this.oppo_player.cards//
        const cards_battle_self=this.table.self_battlefield//再检查battle的
        const cards_battle_oppo=this.table.opponent_battlefield

        const cards=[cards_hand_self,cards_hand_oppo,cards_battle_self,cards_battle_oppo]
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
            console.log(12345)
            return this.table.timmer_turn
        }
        else if(this.table.timmer_bullet.check_inside(mouse_pos,...this.table.timmer_bullet.position_in_screen)){
            console.log(345)
            return this.table.timmer_bullet
        }
        return undefined
    }
    get_mouse_pos(event,canvas){
        var rect = canvas.getBoundingClientRect();
        // 计算鼠标相对于canvas的位置
        var mouseX = (event.clientX - rect.left)*canvas.width/rect.width;
        var mouseY = (event.clientY - rect.top)*canvas.height/rect.height;
        return [mouseX,mouseY]
    }

    judge_move(){
        return true
    }
    judge_click(){
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
}

// (async () => {
//     const client = new GameClient();
//     await client.init();
//     // 现在 client.socket 应该已经准备好了
// })();



const size_rat=7/10;
var SIZE=1000*size_rat;
var POSITION=[2000,-700,3000];
const client = new Game_Client();
function main(){
    
    //await client.init();
    //while (true){
    client.ctx_table.clearRect(0, 0, client.canvas_table.width, client.canvas_table.height);
    client.update()
    client.draw()
    
    
    requestAnimationFrame(main);
}
main()
