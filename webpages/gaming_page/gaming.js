class Game_Client{
    constructor(){
        this.socket_main=null;
        this.socket_select =null;

        this.table=new Table()
        this.canvas_table=this.table.canvas
        this.ctx_table=this.table.ctx
        console.log(this.ctx_table)

        this.set_lestener()


    }
    async init() {
        this.socket_main = await this.get_socket("entering_game");
        this.socket_select = await this.get_socket("select_object");
    }
    async get_socket(name){
        var socket = new WebSocket("ws://127.0.0.1:8000./"+name);
        while (socket.readyState != WebSocket.OPEN){
            await this.sleep(200)
        }
        return socket
    }
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async receive_message_main(){
        while (true){

        }
    }
    async receive_message_select(){
        
    }

    start_drawing(){
        
        this.update();
        this.draw();

        //requestAnimationFrame(this.start_drawing);
    }

    update(){
        this.table.update()
    }
    draw(){
        this.table.draw()
    }
    set_lestener(){
        

        this.canvas_table.addEventListener('mousemove', (event) => {
            
        });
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
            else if (event.key === "p" || event.key === "P") {
                // 执行D键按下时的操作
                this.table.self_battlefield[0].moving_cache.push(["attack_to",[[15,-20,-10]]])
                this.table.self_battlefield[0].moving_cache.push(["rotate_to_point",[[
                    this.table.self_battlefield[0].accurate_position[0],
                    this.table.self_battlefield[0].accurate_position[1],
                    this.table.self_battlefield[0].accurate_position[2]+1,
                ]]])
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
                const card=new Creature_Hand(4,5.62,[0,0,60],1.6,canvas,"3U","Caesar",1122334455)
                const card_battle=new Creature_Battle(6,5,[-25,-25,0],0.3,card,"self",this.table)
                this.table.self_battlefield.push(card_battle)
            }
            else if (event.key === "k" || event.key === "K"){
                const canvas=this.table.card_frame.generate_card("blue","Caesar","creature","Common","shausoaishaisuhai","cards/creature/Angelic Protector/image.jpg")
                const card=new Creature_Hand(4,5.62,[0,0,60],1.6,canvas,"3U","Caesar",1122334455)
                const card_battle=new Creature_Battle(6,5,[-25,-20,0],0.3,card,"opponent",this.table)
                this.table.opponent_battlefield.push(card_battle)
            }

            
        });
        this.canvas_table.addEventListener('mousedown', (event) => { 
            
            
            
                
            
            
        });
        this.canvas_table.addEventListener('mouseup', (event) => {
            
        });

        this.canvas_table.addEventListener('wheel', (event)=> {
            console.log(event.deltaY);
            this.table.camera.angle_x=event.deltaX/40+this.table.camera.angle_x
            this.table.camera.angle_y=event.deltaY/40+this.table.camera.angle_y
            // this.table.camera.add_rotate_prescent(event.deltaY)
            // this.table.camera.update()
           
            event.preventDefault();
        });

        
        

       
        
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
