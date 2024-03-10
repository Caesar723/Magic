
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

async function get_socket(){
    var socket = new WebSocket("ws://127.0.0.1:8000./entering_game");
    while (socket.readyState != WebSocket.OPEN){
        await sleep(200)
    }
    return socket
}


async function main(){
    socket=await get_socket();
    socket.send("Hello, server!");
}
main()
