class Game_Client{
    constructor(){
        this.socket_main=null;
        this.socket_select =null;

        this.table=new Table()
        this.canvas_table=this.table.canvas
        this.ctx_table=this.table.ctx

       
        
        let players=window.dataFromBackend
        
        this.self_player=new Self(players["self"],this.canvas_table,this.ctx_table)
        this.oppo_player=new Opponent(players["opponent"],this.canvas_table,this.ctx_table)
        console.log(this.self_player,this.oppo_player)
        this.table.set_player(this.self_player,this.oppo_player)
        //this.initinal_players()
        

        this.card_frame=new Card_frame()
        this.action_bar=new Action_Bar()
        this.show_2d=new Show_2D(this.canvas_table,this.ctx_table)

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

        this.init()
        

        this.your_turn=true;//判断是不是你的回合
        this.message_processor=new Message_Processor(this)

        
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
        // this.socket_main = await this.get_socket("entering_game");
        // this.socket_select = await this.get_socket("select_object");
        this.get_socket_main()
        await this.get_socket_select()
       
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

    

    receive_message_main_listener(){

        this.socket_main.addEventListener('message', (event)=> {
            console.log('收到消息：', event.data);
            this.message_processor.extractParts(event.data)
            // 在这里处理消息
            // 你可以根据消息的内容执行不同的操作，比如更新UI、存储数据等
          });
        this.socket_main.addEventListener('close', () => {
            console.log('关闭');
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
            this.message_processor.extractParts(event.data)
            // 在这里处理消息
            // 你可以根据消息的内容执行不同的操作，比如更新UI、存储数据等
          });
        this.socket_select.addEventListener('close', () => {
            console.log('关闭');
        });
        this.socket_select.addEventListener('error', (event) => {
            
        });
    }
    massage_process_select(message){

    }

    

    update(){
        this.action_bar.update()
        this.table.update()
        
        this.oppo_player.update()
        this.self_player.update()
        
        this.show_2d.update()
        this.selectionPage.update()

        this.blur_changing()
    }
    draw(){
        //this.ctx_table.filter = 'grayscale(100%)';
        this.table.draw()
        this.oppo_player.draw()
        this.self_player.draw()
        this.ctx_table.filter = 'none';
        if (this.action_bar.mode=="show"){
            this.blur_effect(this.grayscale,this.blur_value)
        }
        this.action_bar.draw(this.canvas_table,this.ctx_table,this.self_player.camera)
        this.show_2d.draw()
        if (this.selectionPage.in_selection && this.selectionPage.selection_mode=="cards" ){
            this.blur_effect(this.grayscale,this.blur_value)
        }
        this.selectionPage.draw()


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
                //this.table.self_battlefield[0].moving_cache.push(["disappear",[[0,-20,-20]]])
                const action=new Die(this.table.self_battlefield[0].card,this.self_player)
                action.set_animate()
                this.action_bar.actions.push(action)
            }
            else if (event.key === "y" || event.key === "Y") {
                // 执行D键按下时的操作
                //this.table.opponent_battlefield[0].start_moving("disappear",[[0,-20,20]])
                const action=new Die(this.table.opponent_battlefield[0].card,this.oppo_player)
                action.set_animate()
                this.action_bar.actions.push(action)
            }
            else if (event.key === "l" || event.key === "L"){
                const canvas=this.table.card_frame.generate_card("blue","Caesar","creature","Common","shausoaishaisuhai","cards/creature/Angelic Protector/image.jpg")
                const card=new Creature_Hand(4,5.62,[0,0,60],1.6,canvas,"3U",20,20,20,20,"Caesar",1122334455)
                const card_battle=new Creature_Battle(6,5,[-25,-25,0],0.3,card,"self",this.table)


                //this.table.self_battlefield.push(card_battle)

                const action=new Summon(card,this.self_player)
                action.set_animate()
                this.action_bar.actions.push(action)
            }
            else if (event.key === "k" || event.key === "K"){
                const canvas=this.table.card_frame.generate_card("blue","Caesar","creature","Common","shausoaishaisuhai","cards/creature/Angelic Protector/image.jpg")
                const card=new Creature_Hand(4,5.62,[0,0,60],1.6,canvas,"3U",20,20,20,20,"Caesar",1122334455)
                const card_battle=new Creature_Battle(6,5,[-25,-20,0],0.3,card,"opponent",this.table)

                const action=new Summon(card,this.oppo_player)
                action.set_animate()
                this.action_bar.actions.push(action)
                //this.table.opponent_battlefield.push(card_battle)
            }
            else if (event.key === "m" || event.key === "M"){
                this.self_player.cards[0].moving_cache.push(["move_to",[[0,0,0]]])
            }
            else if (event.key === "n" || event.key === "N"){
                this.self_player.cards[0].moving_cache.push(["move_to",[[5,0,0]]])
            }
            else if (event.key === "b" || event.key === "B"){
                const canvas_dynamic=this.self_player.card_frame.generate_card("blue","Caesar","creature","Common","shausoaishaisuhai","cards/creature/Angelic Protector/image.jpg")
                const card=new Creature_Hand(4,5.62,[0,60,-20],1.5,canvas_dynamic,"3U",20,20,20,20,"Caesar",1122334455,this.self_player)
        
                //this.self_player.cards.push(card)

                const action=new Gain_Card(this.self_player,this.self_player,card)
                action.set_animate()
                this.action_bar.actions.push(action)
            }
            else if (event.key === "v" || event.key === "V") {
                
                //this.self_player.cards[0].moving_cache.push(["disappear",[[0,60,-20]]])
                const action=new Lose_Card(this.self_player,this.self_player,this.self_player.cards[0])
                action.set_animate()
                this.action_bar.actions.push(action)
            }
            else if (event.key === "c" || event.key === "C") {
                const card=new Card_Hand_Oppo(4,5.62,[0,-60,-20],0.7,1122334455,this.oppo_player)
                const action=new Gain_Card(this.oppo_player,this.oppo_player,card)
                action.set_animate()
                this.action_bar.actions.push(action)
        
                //this.oppo_player.cards.push(card)
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
            else if (event.key === "e" || event.key === "E") {
                //this.table.timmer_turn.animate_set(this.table.timmer_turn.time+5,this.table.timmer_turn.time)
                const action=new Change_Mana(this.self_player,this.self_player,[0,2,15,6,10])
                action.set_animate()
                this.action_bar.actions.push(action)
                //this.self_player.mana_bar.set_mana([0,2,15,6,10])
                //this.oppo_player.cards.push(card)
            }
            else if (event.key === "r" || event.key === "R") {
                
                const action=new Attack_To_Object(this.self_player,this.self_player,this.oppo_player,"rgba(0, 243, 0, 0.9)","Cure",[5])
                action.set_animate()
                this.action_bar.actions.push(action)
                
            }
            else if (event.key === "t" || event.key === "T") {
                
                for (let i in this.table.opponent_battlefield){
                    const action=new Attack_To_Object(this.table.self_battlefield[0].card,this.self_player,this.table.opponent_battlefield[i].card,"rgba(0, 243, 0, 0.9)","Missile_Hit",[5,5])
                    //action.set_animate()
                    this.action_bar.add_actions(action)
                    //this.action_bar.actions.push(action)
                }
                const action=new Attack_To_Object(this.table.self_battlefield[0].card,this.self_player,this.self_player,"rgba(0, 243, 0, 0.9)","Missile_Hit",[5])
                this.action_bar.add_actions(action)
                this.action_bar.add_actions(false)
                // action.set_animate()
                // this.action_bar.actions.push(action)
                
                
            }
            else if (event.key === "[" || event.key === "{") {
                var action_1=new Attack_To_Object(this.self_player,this.self_player,this.oppo_player,"rgba(0, 243, 0, 0.9)","Cure",[5])
                //action.set_animate()
                this.action_bar.add_actions(action_1)
                
                //this.action_bar.actions.push(action)


                var action_2=new Play_Cards(this.self_player.cards[0],this.self_player,this.self_player.cards[0],this.show_2d)
                //action.set_animate()
                //this.action_bar.actions.push(action)
                this.action_bar.add_actions(action_2)

                this.action_bar.add_actions(false)
                var action_1=new Attack_To_Object(this.self_player,this.self_player,this.oppo_player,"rgba(0, 243, 0, 0.9)","Cure",[5])
                //action.set_animate()
                this.action_bar.add_actions(action_1)
                
                //this.action_bar.actions.push(action)


                var action_2=new Play_Cards(this.self_player.cards[1],this.self_player,this.self_player.cards[1],this.show_2d)
                //action.set_animate()
                //this.action_bar.actions.push(action)
                this.action_bar.add_actions(action_2)

                this.action_bar.add_actions(false)

                var action_1=new Attack_To_Object(this.self_player,this.self_player,this.oppo_player,"rgba(0, 243, 0, 0.9)","Cure",[5])
                //action.set_animate()
                this.action_bar.add_actions(action_1)
                
                //this.action_bar.actions.push(action)


                var action_2=new Play_Cards(this.self_player.cards[2],this.self_player,this.self_player.cards[2],this.show_2d)
                //action.set_animate()
                //this.action_bar.actions.push(action)
                this.action_bar.add_actions(action_2)

                this.action_bar.add_actions(false)
                
                
            }
            else if (event.key === "]" || event.key === "】") {
                const canvas=this.table.card_frame.generate_card("blue","Caesar","creature","Common","shausoaishaisuhai","cards/creature/Angelic Protector/image.jpg")
                const card=new Land_Hand(4,5.62,[0,0,60],1.6,canvas,"Caesar",1122334455)
                const card_battle=new Land_Battle(6,5,[-25,-20,0],0.3,card,"self",this.table)


                //this.table.self_battlefield.push(card_battle)

                const action=new Summon(card,this.self_player)
                action.set_animate()
                this.action_bar.actions.push(action)



                const canvas2=this.table.card_frame.generate_card("blue","Caesar","creature","Common","shausoaishaisuhai","cards/creature/Angelic Protector/image.jpg")
                const card2=new Land_Hand(4,5.62,[0,0,60],1.6,canvas2,"Caesar",1122334455)
                const card_battle2=new Land_Battle(6,5,[-25,-20,0],0.3,card2,"opponent",this.table)


                //this.table.self_battlefield.push(card_battle)

                const action2=new Summon(card2,this.oppo_player)
                action2.set_animate()
                this.action_bar.actions.push(action2)
            }
            else if (event.key === "\\" || event.key === "、") {
                const canvas=this.table.card_frame.generate_card("blue","Bacon","creature","Common","shausoaishaisuhai","cards/creature/Aetherweaver/image.jpg")
                const card=new Land_Hand(4,5.62,[0,0,60],1.6,canvas,"Bacon",1122334455)
                const card_battle=new Land_Battle(6,5,[-25,-20,0],0.3,card,"self",this.table)


                //this.table.self_battlefield.push(card_battle)

                const action=new Summon(card,this.self_player)
                action.set_animate()
                this.action_bar.actions.push(action)


                const canvas2=this.table.card_frame.generate_card("blue","Bacon","creature","Common","shausoaishaisuhai","cards/creature/Aetherweaver/image.jpg")
                const card2=new Land_Hand(4,5.62,[0,0,60],1.6,canvas2,"Bacon",1122334455)
                const card_battle2=new Land_Battle(6,5,[-25,-20,0],0.3,card2,"opponent",this.table)


                //this.table.self_battlefield.push(card_battle)

                const action2=new Summon(card2,this.oppo_player)
                action2.set_animate()
                this.action_bar.actions.push(action2)
            }
            else if (event.key === ";" || event.key === ";") {
                
                const action=new Activate_Ability(this.table.self_battlefield[0].card,this.self_player)
                action.set_animate()
                this.action_bar.actions.push(action)

            }
            // else if (event.key === "'" || event.key === "'") {
                
            //     const action=new Activate_Ability(this.table.self_landfield[3].card,this.self_player)
            //     action.set_animate()
            //     this.action_bar.actions.push(action)


            //     const action2=new Reset_Ability(this.table.self_battlefield[0].card,this.self_player)
            //     action2.set_animate()
            //     this.action_bar.actions.push(action2)

            // }
            // else if (event.key === "/" || event.key === "/") {
                
            //     this.message_processor.extractParts("action_list(action(Play_Cards,parameters(Land(0,0,player(CC,Self),int(4319679728),string(Island),blue,Land,Uncommon,string(),cards/land/Island/image.jpg),player(CC,Self),showOBJ())),action(Lose_Card,parameters(player(CC,Self),player(CC,Self),Opponent(player(CC,Self),int(4319679728)))),action(Summon,parameters(Land(0,0,player(CC,Self),int(4319679728),string(Island),blue,Land,Uncommon,string(),cards/land/Island/image.jpg),player(CC,Self))))")


            // }
            else if (event.key === "'" || event.key === "'") {
                
                this.self_player.player_life_ring.change_blue()


            }
            else if (event.key === "/" || event.key === "/") {
                
                this.self_player.player_life_ring.change_orange()


            }



            
        });
        this.canvas_table.addEventListener('mousedown', (event) => { 
            const mouse_pos=this.get_mouse_pos(event,this.canvas_table)
            const card=this.find_cards_by_mouse(mouse_pos)
            const timer=this.find_timers_by_mouse(mouse_pos)

            const object=this.selectionPage.check_mouse_in_selection(mouse_pos)
            if (object===undefined && this.selectionPage.in_selection){
                this.resolveSelectInput("cancel_client")
            }
            else if (! (object===undefined)){
                this.end_selection(object)
            }
            else if (! (card===undefined)){
                //console.log(card)
                const click_bool=this.judge_click(card)
                const move_bool=this.judge_move(card)
                this.card_hold=[card,click_bool,move_bool]
                card.card_hold=[click_bool,move_bool]
                
            }
            this.startTime = performance.now();

            if (!(timer===undefined)){
                this.end_time(timer)
                
            }
            
            
            
            
        });
        this.canvas_table.addEventListener('mousemove', (event) => {
            
            if (this.card_hold[2]){
                this.show_2d.delete_mouse_card()
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

                const object=this.selectionPage.check_mouse_in_selection(mouse_pos)



                if ( ((!(card===undefined)||!(timer===undefined))&&!this.selectionPage.in_selection) || (this.selectionPage.in_selection&&!(object===undefined)) ){
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
        this.canvas_table.addEventListener('mouseup', (event) => {
            if (!(this.card_hold[0]===undefined)){
                
                
                if (this.card_hold[0] instanceof Card_Battle){
                    this.card_hold[0].angle_x=math.pi/2;;
                    this.card_hold[0].angle_y=0;
                    this.card_hold[0].angle_z=0;
                    if (performance.now()-this.startTime<0.15*1000){
                        if (this.card_hold[1]){
                            this.battle_click_activate(this.card_hold[0])
                        }
                    }
                    else{
                        if (this.card_hold[2]){
                            this.battle_move_activate(this.card_hold[0])
                        }
                    }
                    
                    
                    

                    
                }
                else if(this.card_hold[0] instanceof Card_Hand){
                    this.card_hold[0].angle_x=0;
                    this.card_hold[0].angle_y=0;
                    this.card_hold[0].angle_z=0;
                    if (performance.now()-this.startTime<0.15*1000){
                        this.self_player.change_to_focus()
                    }
                    else{
                        this.hand_move_activate(this.card_hold[0])
                    }
                    // if (this.card_hold[1]){
                        
                    // }
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
            //this.table.camera.angle_x=event.deltaX/40+this.table.camera.angle_x
            //this.table.camera.angle_y=event.deltaY/40+this.table.camera.angle_y
            if (this.selectionPage.in_selection==false){
                this.table.camera.add_rotate_prescent(event.deltaY)
                this.table.camera.update()
            }
            

            this.selectionPage.rotate_cards(event.deltaX)
           
            event.preventDefault();
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
        if (card instanceof Creature_Battle && ((card.position_in_screen[1][1]+card.position_in_screen[2][1])/2<this.canvas_table.height/3)){
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
    hand_move_activate(card){
        console.log((card.position_in_screen[1][1]+card.position_in_screen[2][1])/2<this.canvas_table.height/3)
        if ((card.position_in_screen[1][1]+card.position_in_screen[2][1])/2<this.canvas_table.height/3){
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
