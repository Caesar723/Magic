
// function set_Listener(){
    
// }
// set_Listener();
// 在 JavaScript 文件都注册相同的 Service Worker
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('webpages/service-worker.js').then(function(registration) {
        console.log('Service Worker registered with scope:', registration.scope);
    });
}
const decks=new Decks_Container()
const home= new Home(decks)

function draw_picture(){
        
        decks.draw()
        
        requestAnimationFrame(draw_picture);
    }
    
    draw_picture()