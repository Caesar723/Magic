class Deck{

    constructor(name,content,Container,id){
        this.Container=Container
        this.id=id
        this.canvas = document.createElement('canvas');
        this.canvas.className = "canvas_deck";
        this.ctx = this.canvas.getContext("2d");
        this.cards=[];
        this.name=name;
        this.process(content);
        this.div_button_ini()
    }
    async get_canvas(){
       


    }
    process(content){
        for (let i in content){
            this.cards.push(new Card(content[i].name,content[i].type_card,content[i].quantity));
        }
    }
    div_button_ini(){
        const box_decks=document.getElementById('box_decks');
        this.divbutton = document.createElement("div");
        this.divbutton.className = "button_deck";
        

        const text=document.createElement("span");
        text.className = "text_deck";
        text.textContent = this.name;
        this.divbutton.appendChild(text)
        this.divbutton.addEventListener('click',(event)=> {
            console.log(event.currentTarget)
            console.log(this)
            document.getElementById('button_process').classList.add('show_button_process');
            this.clear_child("button_process_deck_click")
            event.currentTarget.classList.add('button_process_deck_click');
            this.change_box(event)
        })
        box_decks.appendChild(this.divbutton)
    }

    change_box(event){
        
        const box_cards_1=document.getElementById('box_cards_1');
        const box_cards_2=document.getElementById('box_cards_2');

        if (box_cards_1.classList.contains('box_cards_front')) {
            box_cards_2.classList.add('box_cards_front');
            box_cards_1.classList.remove('box_cards_front');
            this.replace_child(box_cards_2)
        }
        else if(box_cards_2.classList.contains('box_cards_front')){
            box_cards_1.classList.add('box_cards_front');
            box_cards_2.classList.remove('box_cards_front');
            this.replace_child(box_cards_1)
        }
        else{
            box_cards_1.classList.add('box_cards_front');
            this.replace_child(box_cards_1)
        }

    }
    replace_child(box_cards){
        if (box_cards.hasChildNodes()){
            box_cards.removeChild(box_cards.firstChild);
        }
        box_cards.appendChild(this.canvas)

    }

    draw_canvas(){
        
        this.ctx.clearRect(0,0,this.canvas.width,this.canvas.height);
        this.ctx.save();
        
        this.canvas.height=window.innerHeight;
        this.canvas.width=window.innerWidth/6;

        for(let card_i in this.cards){
            const ratio=this.canvas.width/this.cards[card_i].canvas.width;
            console.log(this.canvas.width, this.cards[card_i].canvas.height*ratio)
            this.ctx.drawImage(this.cards[card_i].canvas,
                0,card_i*this.cards[card_i].canvas.height*ratio*1.1,
                this.canvas.width,
                this.cards[card_i].canvas.height*ratio
                )
        }

        this.ctx.restore();
    }

    clear_child(class_name){
        for (let i in this.Container.all_decks){
            const deck=this.Container.all_decks[i];
            deck.divbutton.classList.remove(class_name);
        }
    }

}

class Card{
    constructor(name,type,quantity){
        this.name=name
        this.type=type
        this.quantity=quantity
        this.img_path= `cards/${type}/${name}/compress_img.jpg`
        
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext("2d");
        this.canvas.width = 1470*0.2;
        this.canvas.height = 60;

        this.load_img()
    }
    load_img(){
        var img = new Image();
        this.img=NaN
        img.onload= ()=>{
            this.img=img
            this.draw(img)
            console.log(2)
        }
        img.src = this.img_path;

    }
    draw(img){
        this.ctx.clearRect(0,0,this.canvas.width,this.canvas.height)
        this.ctx.save();
        this.roundedRect(this.ctx,0,0,this.canvas.width,this.canvas.height,20)
        this.ctx.fillStyle = "rgb(33,33,33,0.85)";
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height); // 画一个长方形
        this.ctx.fillStyle = "rgb(173,173,173,0.85)"; // 设置填充颜色为红色
        this.ctx.fillRect(this.canvas.width*0.8, 0, this.canvas.width*0.2, this.canvas.height); // 画一个长方形
        this.ctx.font = '20px Merriweather';
        this.ctx.fillStyle = "rgb(233,233,233,0.85)"; // 设置字体颜色
        this.drawTextWithEllipsis(this.ctx, this.name, 70, 40, 150);
        this.ctx.font = '35px Merriweather';
        this.ctx.fillStyle = "rgb(33,33,33,0.85)"; // 设置字体颜色
        this.ctx.fillText(this.quantity.toString(), this.canvas.width*0.85, 40);

        // 绘制文本
        //this.ctx.fillText('Hello, Canvas!', 10, 50);
        
        
        this.ctx.drawImage(img,0, 0, img.width,img.height, 0,0, this.canvas.height, this.canvas.height)
        
        
        //ctx.drawImage(this.canvas,...position,this.canvas.width,this.canvas.height)
        
    }
    drawTextWithEllipsis(ctx, text, x, y, maxWidth) {
        const metrics = ctx.measureText(text);
        if (metrics.width <= maxWidth) {
            ctx.fillText(text, x, y);
        } else {
            let adjustedText = text;
            while (ctx.measureText(adjustedText + '...').width > maxWidth) {
                adjustedText = adjustedText.slice(0, -1);
            }
            ctx.fillText(adjustedText + '...', x, y);
        }
    }
    roundedRect(ctx, x, y, width, height, radius) {
        ctx.beginPath();
        ctx.moveTo(x + radius, y);
        ctx.lineTo(x + width - radius, y);
        ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
        ctx.lineTo(x + width, y + height - radius);
        ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
        ctx.lineTo(x + radius, y + height);
        ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
        ctx.lineTo(x, y + radius);
        ctx.quadraticCurveTo(x, y, x + radius, y);
        ctx.closePath();
        ctx.clip();
      }
}