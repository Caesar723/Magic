
// function set_Listener(){
    
// }
// set_Listener();

const decks=new Decks_Container()
const home= new Home(decks)

function draw_picture(){
        
        decks.draw()
        
        requestAnimationFrame(draw_picture);
    }
    
    draw_picture()