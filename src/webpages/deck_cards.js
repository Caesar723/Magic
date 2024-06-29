class Deck{

    constructor(){
        this.canvas = document.getElementById("deckCanvas");
        this.ctx = this.canvas.getContext("2d");
        this.canvas.width = 1470*0.2;
        this.canvas.height = 742;
        this.background=this.initinal_deck()

        this.offset=0
        this.cards={
        }


        
    }

    push_card(card){
        const name_index=card.name+"_"+card.constructor.name
        
        if (name_index in this.cards){
            this.cards[name_index].quantity++
        }
        else{
            this.cards[name_index]=new Card_In_Deck(card)
        }
        
    }
    
    update(){
        
    }
    check_empty(){
        if (Object.keys(this.cards).length === 0){
            return true
        }
        else{
            return false
        }
    }
    draw(){
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.save();
        //this.ctx.fillStyle = "rgb(218,218,173,0.9)"; // 使用CSS颜色值，这里为CornflowerBlue
        //this.ctx.drawImage(0, 0, this.canvas.width, this.canvas.height)
        this.ctx.drawImage(this.background,0, 0, this.canvas.width, this.canvas.height); // 绘制一个覆盖整个Canvas的矩形
        this.draw_cards()
        this.ctx.restore();
    }
    draw_cards(){
        Object.keys(this.cards).forEach((key, i) => {
        //for (let i in this.cards){
            const y_pos=i*70+this.offset+this.canvas.height*0.1
            if (y_pos<this.canvas.height && y_pos>0){
                this.cards[key].draw_a_card(this.ctx,[0,y_pos])
            }
            
            
        })
    }

    
    initinal_deck(){
        var img = new Image();
        
        img.src = 'webpages/deckpage/deck.PNG'; // 替换为你的图片路径
        var canvas_2 = document.createElement('canvas');
        canvas_2.width = this.canvas.width;
        canvas_2.height = this.canvas.height;
        var ctx_2 = canvas_2.getContext("2d");
        img.onload = function() {
            ctx_2.drawImage(img, 0, 0, canvas_2.width, canvas_2.height);
        }
        
        return canvas_2;
    }

    check_mouse(mouse_pos){

        if (mouse_pos[0]>1470*0.8 && mouse_pos[1]>this.canvas.height*0.1){
            Object.keys(this.cards).forEach((key, i) => {
                const y_pos=i*70+this.offset+this.canvas.height*0.1

                if (y_pos+this.cards[key].canvas.height>mouse_pos[1] && y_pos<mouse_pos[1]){
                    this.delete_card(this.cards[key],key)
                    //console.log(this.cards[key],y_pos,y_pos+this.cards[key].canvas.height,mouse_pos[1])
                }
            })
        }
        return false
    }
    delete_card(card_deck,key){
        if (card_deck.quantity==1){
            delete this.cards[key]
        }
        else{
            card_deck.quantity--
        }
        card_deck.card.quantity++
    }

    async settle_deck(deck_name){// name+type+quality|...
        var result_text=deck_name;
        for (let key in this.cards){
            const total_detail=this.cards[key].name+"+"+this.cards[key].card.constructor.name+"+"+this.cards[key].quantity
            result_text=result_text+"|"+total_detail
            
        }
        console.log(result_text)
        return await this.encryptWithAES(result_text)
    }

    async encrypt(message,pem){
        const publicKey=await this.importPublicKey(pem)
        console.log(publicKey)
        const encoder = new TextEncoder();
        const encodedMessage = encoder.encode(message);
        console.log(1)
        const encryptedMessage = await window.crypto.subtle.encrypt(
            {
                name: 'RSA-OAEP',
            },
            publicKey,
            encodedMessage
        );
        console.log(2)
        return this.arrayBufferToBase64(new Uint8Array(encryptedMessage));
    }
    async importPublicKey(pem) {
        const binaryDer = window.atob(pem.split('\n').slice(1, -2).join(''));
        const array = new Uint8Array(binaryDer.length);
        for (let i = 0; i < binaryDer.length; i++) {
            array[i] = binaryDer.charCodeAt(i);
        }
        return window.crypto.subtle.importKey(
            'spki',
            array.buffer,
            {
                name: 'RSA-OAEP',
                hash: 'SHA-256',
            },
            false,
            ['encrypt']
        );
    }
    arrayBufferToBase64(buffer) {
        let binary = '';
        const bytes = new Uint8Array(buffer);
        const len = bytes.byteLength;
        for (let i = 0; i < len; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return window.btoa(binary);
    }

    
    async encryptWithAES(secretData) {
        const encoder = new TextEncoder();
        const data = encoder.encode(secretData);

        // 生成密钥和初始化向量(IV)
        const key = await window.crypto.subtle.generateKey(
            { name: "AES-CBC", length: 256 },
            true,
            ["encrypt", "decrypt"]
        );
        
        const exportedKey = await window.crypto.subtle.exportKey("raw", key);
        console.log(exportedKey)
        const iv = window.crypto.getRandomValues(new Uint8Array(16));

        // 加密数据
        const encryptedData = await window.crypto.subtle.encrypt(
            { name: "AES-CBC", iv },
            key,
            data
        );

        // 将ArrayBuffer转换为Base64
        // const base64EncryptedData = btoa(String.fromCharCode.apply(null, new Uint8Array(encryptedData)));
        // const base64IV = btoa(String.fromCharCode.apply(null, iv));
    
        
        const result=this.arrayBufferToBase64(exportedKey)+";"+this.arrayBufferToBase64(iv)+";"+this.arrayBufferToBase64(encryptedData)
        return result;
    }

    encrypt_base64(message) {
        return btoa(message)
    }
}

class Card_In_Deck{


    constructor(card){
        this.card=card
        this.orginal_image=card.orginal_image
        this.quantity=1
        this.name=card.name
        this.canvas= document.createElement('canvas');;
        this.ctx = this.canvas.getContext("2d");
        this.canvas.width = 1470*0.2;
        this.canvas.height = 60;
    }


    draw_a_card(ctx,position){
        
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
        
        
        this.ctx.drawImage(this.orginal_image,0, 0, this.orginal_image.width,this.orginal_image.height, 0,0, this.canvas.height, this.canvas.height)
        
        
        ctx.drawImage(this.canvas,...position,this.canvas.width,this.canvas.height)
        this.ctx.restore();
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
}
