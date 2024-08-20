if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('webpages/service-worker.js').then(function(registration) {
        console.log('Service Worker registered with scope:', registration.scope);
    });
}

function set_Listener(){
    const draw = document.getElementById('exit');
    draw.addEventListener('click',  function () {
            window.location.href = '/';
    });
}

set_Listener();
const frame_generator=new Card_frame()
const paras=[
    ["blue","Caesar","Creature","Uncommon","nothing nothing","cards/creature/Spectral Harbinger/image.jpg"],
    ["red","Caesar","Creature","Mythic Rare","nothing nothing","cards/creature/Eternal Phoenix/image.jpg"],
    ["black","Caesar","Creature","Common","nothing nothing","cards/creature/Nyxborn Serpent/image.jpg"],
    ["gold","Caesar","Creature","Rare","nothing nothing","cards/creature/Luminous Guardian/image.jpg"],
    ["green","Caesar","Creature","Mythic Rare","nothing nothing","cards/creature/Verdant Wyrm/image.jpg"]
]


const camera=new Camera([0,0,-50])
const deck=new Deck()
const book=new Book(camera,deck)


var startTime = performance.now();
function draw_picture(){
    const endTime = performance.now();
    const runningTime = endTime - startTime;
    
    //console.log(runningTime)
    if (runningTime>0.01*1000){
        startTime = performance.now();
        book.update();
        deck.update();
        book.draw();
        deck.draw();
        
    }
    

    
    requestAnimationFrame(draw_picture);
}

draw_picture()