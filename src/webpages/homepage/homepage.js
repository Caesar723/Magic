if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('webpages/service-worker.js').then(function(registration) {
        console.log('Service Worker registered with scope:', registration.scope);
    });
}
// function set_Listener(){
    
// }
// set_Listener();
// 在 JavaScript 文件都注册相同的 Service Worker

    // Start Generation Here
 async function get_currency() {
    const currency=await fetch('/get_currency',{
        method:'POST',
    })
    const data=await currency.json()
    const element=document.getElementById('currency')
    const span=element.querySelector('.button-text')
    console.log(element)
    span.innerHTML=`<img src="webpages/homepage/coin.png" alt="Description" id="img_coin">${data.currency}`
    
}








get_currency()
const decks=new Decks_Container()
const home= new Home(decks)

function draw_picture(){
        
    decks.draw()
    
    requestAnimationFrame(draw_picture);
}
    
draw_picture()