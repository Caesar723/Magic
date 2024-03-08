

class Button{

    constructor(x,y,height,length){
        this.x=x;
        this.y=y;
        this.height=height;
        this.length=length;
    }

    clicked(){
        
    }
    check_mouse(mouse_pos){
        if (mouse_pos[0]>this.x && mouse_pos[0]<this.x+this.length && mouse_pos[1]>this.y && mouse_pos[1]<this.y+this.height){
            return true;
        }
        else{
            return false;
        }
    }
}