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
        });
        this.canvas_table.addEventListener('mousedown', (event) => { 

        });
        this.canvas_table.addEventListener('mouseup', (event) => {
            
        });

        this.canvas_table.addEventListener('wheel', (event)=> {
            console.log(event.deltaY);
            // this.table.camera.angle_x=event.deltaX/40+this.table.camera.angle_x
            // this.table.camera.angle_y=event.deltaY/40+this.table.camera.angle_y
            this.table.camera.add_rotate_prescent(event.deltaY)
            this.table.camera.update()
           
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
